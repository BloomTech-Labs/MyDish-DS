import numpy as np
from flask import Flask, jsonify, request


app = Flask(__name__)

# create root route
@app.route('/')
@app.route('/home')
def home():
    mock_data = ({

        'id': '1',
        'dish': 'taco',
                'ingredient': 'meat, tomato, shell',
                'instructions': '1. cook, 2. add stuff, 3.eat',
                'measurements': '.5 pounds, 1 tomato, 1 taco shell'


    })
    return mock_data


@app.route('/object_detection')
def detect():
    message = 'To Be Implemented.'
    return message


@app.route('/vision')
def vision():
    message = 'Work In Progress.'
    return message


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
