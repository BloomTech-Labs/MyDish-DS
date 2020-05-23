import time
import os
import numpy as np
import cv2
from absl import app, logging
import json


import tensorflow as tf
from yolov3_tf2.models import YoloV3, Yolov3Tiny

'''
Endpoint that returns the images with the detection: bound-boxing, accuracy, class name.
'''


def image_detection():
    '''
    Returns images with the detection: bound-boxing, accuracy, class name.
    '''
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
            res_i = jsonify({"Response": response}), 200
            return json.dump(res_i)
        except FileNotFoundError:
            abort(404)
