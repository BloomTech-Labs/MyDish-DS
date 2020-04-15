"""
Vision endpoint for heroku. For RC1 we should at minimum be able to deploy
to heroku as we get comfortable with AWS.
"""
from google.cloud import vision
import processing
import json
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

# Blueprint connection
vision_routes = Blueprint("vision_routes", __name__)


@visions_enpoint.route('/visions')
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
