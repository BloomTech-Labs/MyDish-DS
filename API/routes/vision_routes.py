"""
Vision endpoint for heroku. For RC1 we should at minimum be able to deploy
to heroku as we get comfortable with AWS.
"""
from flask import Blueprint, request, jsonify
from google.cloud import vision
import transform
import json
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

# Blueprint connection
vision_routes = Blueprint("vision_endpoint.routes", __name__)


@vision_endpoint.route('/', methods=['GET'])
def image_parse(uri):
    '''
    Makes a call to Google Vision's OCR API and parses all identifiable text from an image file.
    :param uri: Takes in URI object where image file is located.
    :return: Returns blocks of text obtained from the Google Vision API.
    '''

    # Vision API call using URI
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri
    response = client.document_text_detection(image=image)

    texts = response.text_annotations
    recipe = str(texts[0].description)

    response = processing.main_function(recipe)

    app_json = json.dumps(response)
    return app_json


# ScottLightfoot code
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
        "1": "butter",
        "2": "chocolate",
        "3": "sugar"
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
