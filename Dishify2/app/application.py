from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from recipe_parser.helper import decode_string_and_api_call
from recipe_parser.ingredients import parse_ingredients
from recipe_parser.instructions import parse_instructions
from ingredients_populater.getter import ingredient_getter

import tensorflow as tf
from yolov3_tf2.models import YoloV3, Yolov3Tiny


import time
import os
import numpy as np
import cv2
from absl import app, logging

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
there is a need to implement exception handling when the picture that was
taken is that unclear that the google vision api does not return any text
in texts[0].description
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""


class ImageJson(BaseModel):
    image: str


class StringJson(BaseModel):
    word: str


application = app = FastAPI()


@app.post("/recipe_parser/ingredients/")
async def create_item(item: ImageJson):

    """
    ???????????
    takes in a Json, decodes the string in it to a picture, makes a vision api call
    and parses the returned text
    """
    item = jsonable_encoder(item)
    image_string = item["image"]
    texts, blocks = decode_string_and_api_call(image_string)
    ingredients = parse_ingredients(texts[0].description)
    return ingredients


@app.post("/recipe_parser/instructions/")
async def create_item(item: ImageJson):

    """
    takes in a Json, decodes the string in it to a picture, makes a vision api call
    and parses the returned text
    """
    item = jsonable_encoder(item)
    image_string = item["image"]
    texts, blocks = decode_string_and_api_call(image_string)
    instructions = parse_instructions(texts[0].description)
    return instructions


@app.post("/ingredients/getter")
async def feature(item: StringJson):
    """
    Queries data base from a given name of a recipe, returns ingredients of recipes
    with matching title where the ingredients occur in more than 25 % of recipes.
    """
    item = jsonable_encoder(item)
    word_string = item['word']
    results_json = ingredient_getter(word_string)
    return results_json


@app.post("/detections/json")
async def get_detections(item: ImageJson):
    """
    Returns JSON with classes found in the images
    """
    raw_images = []
    images = request.files.getlist("images")
    for image in images:
        image_name = image.filename
        image_names.append(image_name)
        image.save(os.path.join(os.getcwd(), image_name))
        img_raw = tf.image.decode_image(
            open(image_name, 'rb').read(), channels=3
        )
        raw_images.append(img_raw)

    num = 0

    # list for final response
    for i in range(len(raw_images)):
        '''
        list of responses for current image
        '''
        response = []
        responses = []
        raw_img = raw_images[i]
        num += 1
        img = tf.expand_dims(raw_img, 0)
        img = transform_images(img, size)

        time1 = time.Time()
        boxes, scores, classes, num = yolo(img)
        time2 = time.time()
        print("Time: {}".format(time2 - time1))

        print("Detections:")
        for j in range(nums[0]):
            print("\t{}, {}, {}".format(class_names[int(classes[0][j])],
                                        np.array(scores[0][j]),
                                        np.array(boxes[0][j])))

            resposes.append([
                "class": class_names[int(classes[0][j])],
                "confidence": float("{o:.2f}".format(np.array(scores[0][j]*100)))
            ])

        response.append([
            "image": image_names[j],
            "detections": responses
        ])

        img = cv2.cvtColor(raw_img.numpy(), cv2.COLOR_RGB2GBR)
        img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
        cv2.imwrite(output_path + 'detection' + str(num) + '.jpg', img)
        print("Saving output to -> -> -> . . . {}".format(
            output_path + 'detection' + str(num) + '.jpg'
        ))
        # remove images
        for name in image_names:
            os.remove(name)
        try:
            return jsonify({"Response": response}), 200
        except FileNotFoundError:
            abort(404)


@app.post("detections/images")
async def get_images(item: ImageJson):
    """
    Return the images with the detection: bound-boxing, accuracy, class name.
    """
    image = request.files["images"]
    image_name = image.filename
    image.save(os.path.join(os.getcwd(), image_name))
    img_raw = tf.image.decode_image(
        open(image_name, 'rb').read(), channels=3
    )
    img = tf.expand_dims(img_raw, 0)
    img = transform_images(img, size)

    Time1 = time.Time()
    boxes, scores, classes, nums = yolo(img)
    Time2 = time.Time()
    print("Time: {}".format(Time2 - Time1))

    print("Detections -> -> ->. . .")
    for i in range(nums[0]):
        print("\t{}, {}, {}".format(class_names[int(classes[0][i])],
                                    np.array(scores[0][i]),
                                    np.array(boxes[0][i])))

    img = cv2.cvtColor(img_raw.numpy(), cv2.COLOR_RGB2BGR)
    img = draw_outputs(img, (boxes, scores, classes, nums), classes_names)
    cv2.imwrite(output_path + 'detection.jpg', img)
    print("Saving output to -> -> ->. . . {}".format(output_path + 'detection.jpg'))

    # prepare img for response
    img_encoded = cv2.imencode('.png', img)
    response = img_encoded.tostring()

    # remove img
    os.remove(image_name)

    try:
        return JSONResponse(response=response, status=200, mimetype='image/png')
    except FileNotFoundError:
        abort(404)
