from flask import Flask, render_template, request
import imageio
from PIL import Image 
import random
from google.cloud import storage
import re
import base64
import sys 
import os
import time
from multiprocessing import Process
import requests

app = Flask(__name__)

DEBUG = True
CLOUD_STORAGE_ENABLED = True

#GCP Application Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "auth/storage-admin.json"

#Prediction REST API URL
PREDICT_REST_API_URL = os.environ["PREDICT_REST_API_URL"]
    
@app.route('/')
def index():
    print("Index page rendering...")
    return render_template("index.html") 

@app.route('/predict/', methods=['GET','POST'])
def predict():
    transaction_id = str(int(time.time()*1000000))
    if DEBUG: print(f'transaction_id={transaction_id}')

    filename = transaction_id + '.png'
    folder = 'static/digits/'
    localImagePath = folder + filename

    save_image(localImagePath, request.get_data())
    if DEBUG: print(f'localImagePath={localImagePath}')

    image = open(localImagePath, "rb").read()
    file_payload = {"image": image}
    parameter_payload = {"transaction_id": transaction_id}

    response = requests.post(PREDICT_REST_API_URL, files=file_payload, data=parameter_payload)
    response = response.json()
    if DEBUG: print(response)

    if response["success"]:
        out = response["predicted_digit"]
    else:
        out = -1

    response = str(out)

    if CLOUD_STORAGE_ENABLED:   
        async_process = Process(  # Create a daemonic async process
            target=upload_to_gcp,
            args=(localImagePath, ),
            daemon=True
        )
        async_process.start()
        
    return response 
    
def save_image(localImagePath, imgData):
    imgstr = re.search(b'base64,(.*)', imgData).group(1)

    with open(localImagePath,'wb') as output:
        output.write(base64.decodebytes(imgstr))

def upload_to_gcp(file, remove_after_upload=True):
    client = storage.Client() 
    bucket = client.get_bucket("dsp-sudoku")

    blob = bucket.blob('predicted/' + file.split('/')[-1])
    blob.upload_from_filename(file)
    blob.make_public()

    url = blob.public_url
    if DEBUG: print(f"Cloud Public Image URL={url}")

    if remove_after_upload:
        os.remove(file)

    return url
    
if DEBUG: print("DEBUG Enabled")
if CLOUD_STORAGE_ENABLED: print("CLOUD_STORAGE_ENABLED Enabled")

#Used while testing locally with flask
if __name__ == '__main__':
    os.environ['PREDICT_REST_API_URL'] = "http://localhost:5000/predict"
    app.run(debug=True, host='0.0.0.0', port=8080)

#Used while running on Docker with gunicorn
if __name__ == "app" :
    print("Initializing the service.")

