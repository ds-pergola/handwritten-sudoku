from flask import Flask, render_template, request
import imageio
from PIL import Image 
import numpy as np
import uuid
import random
from google.cloud import storage
import re
import base64
import sys 
import os
import time
sys.path.append(os.path.abspath("./model"))

app = Flask(__name__)

DEBUG = True
CLOUD_STORAGE_ENABLED = True
    
@app.route('/')
def index():
    print("Index initialized.")
    return render_template("index.html") 

@app.route('/predict/', methods=['GET','POST'])
def predict():
    # transaction_id = str(uuid.uuid4())
    transaction_id = str(int(time.time()*1000000))
    if DEBUG: print(f'transaction_id={transaction_id}')

    localImagePath = saveImage(transaction_id, request.get_data())
    if DEBUG: print(f'localImagePath={localImagePath}')

    # read parsed image back in 8-bit, black and white mode (L)
    x = imageio.imread(localImagePath, pilmode="L")
    x = np.invert(x)
    x = np.array(Image.fromarray(x).resize(size=(28, 28)))

    out = random.randint(1, 9)

    # response = np.array_str(np.argmax(out, axis=1))
    response = str(out)

    if CLOUD_STORAGE_ENABLED:   # Remove local file
        os.remove(localImagePath)

    return response 
    
def saveImage(transaction_id, imgData):
    imgstr = re.search(b'base64,(.*)', imgData).group(1)
    folder = 'static/digits/' 
    filename = transaction_id + '.png'
    localImagePath = folder + filename

    with open(localImagePath,'wb') as output:
        output.write(base64.decodebytes(imgstr))

    if CLOUD_STORAGE_ENABLED:
        upload_to_gcp(localImagePath)
    
    return localImagePath


def upload_to_gcp(file):
    client = storage.Client.from_service_account_json('auth/DSPergola_storage-admin.json')
    bucket = client.get_bucket("dsp-sudoku")

    blob = bucket.blob('predicted/' + file.split('/')[-1])
    blob.upload_from_filename(file)
    blob.make_public()

    url = blob.public_url
    if DEBUG: print(f"Cloud Public Image URL={url}")


if __name__ == '__main__':
    if DEBUG: print("DEBUG Enabled")
    if CLOUD_STORAGE_ENABLED: print("CLOUD_STORAGE_ENABLED Enabled")

    app.run(debug=True, host='0.0.0.0', port=8080)
    #app.run(debug=True)
