from flask import Flask, render_template, request
import imageio
from PIL import Image 
import numpy as np
import uuid
import random

# import keras.models
import re
import base64

import sys 
import os
import time
sys.path.append(os.path.abspath("./model"))
# from load import *

app = Flask(__name__)
# global model, graph
# model, graph = init()
    
@app.route('/')
def index():
    print("Index initialized.")
    return render_template("index.html") 

@app.route('/predict/', methods=['GET','POST'])
def predict():
    # transaction_id = str(uuid.uuid4())
    transaction_id = str(int(time.time()*1000000))
    print(transaction_id)

    parseImage(transaction_id, request.get_data())

    # read parsed image back in 8-bit, black and white mode (L)
    x = imageio.imread('digits/'+transaction_id+'.png', pilmode="L")
    x = np.invert(x)
    x = np.array(Image.fromarray(x).resize(size=(28, 28)))

    out = random.randint(1, 9)

    # response = np.array_str(np.argmax(out, axis=1))
    response = str(out)
    return response 
    
def parseImage(transaction_id, imgData):
    # parse canvas bytes and save as output.png
    imgstr = re.search(b'base64,(.*)', imgData).group(1)
    with open('digits/'+transaction_id+'.png','wb') as output:
        output.write(base64.decodebytes(imgstr))

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
