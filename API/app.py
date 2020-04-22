import numpy as np
import json

from flask import Flask, jsonify, request
from tensorflow.keras.models import load_model

'''
ScottLightfoot Baseline Model. We will consider this our baseline instead of
the Dishify api.
'''

app = Flask(__name__)

# create root route
@app.route('/')
def home():
    barebone_api = '<h1>Deleting all the mess I made. Waiting for Robins FastAPI deployment.</h1>'
    return barebone_api


if __name__ == '__main__':
    app.run(debug=True)
