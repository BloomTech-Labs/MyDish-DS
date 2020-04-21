#import pandas as pd
from flask import Flask, jsonify, request
from google.cloud import vision
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ProjectKey.json"

# app
app = Flask(__name__)

# routes


@app.route('/', methods=['GET'])
def predict():
    # get data
    #     data = request.get_json(force=True)
    uri = 'https://schermerhorn.pbworks.com/f/1478276442/procedure1.PNG'

    # limit to 10 MB json file?

    # vision call
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri
    response = client.document_text_detection(image=image)

    recipe_blocks = len(response.full_text_annotation.pages[0].blocks)
    recipe_texts = []

    for block in response.full_text_annotation.pages[0].blocks:

        blocktext = []

        for paragraph in block.paragraphs:

            for word in paragraph.words:

                wordtext = ''
                for symbol in word.symbols:
                    wordtext += symbol.text

                blocktext.append(wordtext)

        recipe_texts.append(blocktext)

    recipe_dict = {'blocks': recipe_blocks, 'texts': recipe_texts}

    # return data
    return jsonify(results=recipe_dict)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
