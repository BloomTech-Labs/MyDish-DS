import numpy as np
import json

from flask import Flask, jsonify, request
from tensorflow.keras.models import load_model

application = Flask(__name__)

with open('ingr_int.json') as json_file:
    ingr_int = json.load(json_file)
with open('int_ingr.json') as json_file:
    int_ingr = json.load(json_file)

my_model = load_model('baseline_pred.h5')
max_pred_length = 10

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def pred_next_ingr(ingr_list):

    pred_next = []

    for diversity in [0.2, 0.6, 1.2]:

        start_ingr = [ingr_int[x] for x in ingr_list]
        
        for i in range(10):
            x_pred = np.zeros((1, max_pred_length, len(ingr_int)))
            for t, ingr in enumerate(start_ingr):
                x_pred[0, t, ingr] = 1

            preds = my_model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_ingredient = int_ingr[str(next_index)]

            pred_next.append(next_ingredient)

    return list(set(pred_next))

@application.route('/', methods=['GET'])
def return_conf():
    return 'aight, now what?'

@application.route('/pred', methods=['GET'])
def return_sample():
    
    sample_json = {
        "1":"butter", 
        "2":"chocolate",
        "3":"sugar"
    }

    ingr_list = list(sample_json.values())
    next_preds = pred_next_ingr(ingr_list)

    next_preds = (set(next_preds) - set(ingr_list))

    return jsonify(list(next_preds))


@application.route('/pred', methods=['POST'])
def return_prediction():
    
    ingr_inputs = request.get_json(force=True)
    ingr_inputs.update((x, y) for x, y in ingr_inputs.items())

    ingr_list = list(ingr_inputs.values())
    next_preds = pred_next_ingr(ingr_list)

    next_preds = (set(next_preds) - set(ingr_list))
    
    return jsonify(list(next_preds))

if __name__ == '__main__':
    application.run(debug=True, port=8000)

