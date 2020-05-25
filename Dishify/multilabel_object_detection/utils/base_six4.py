import base64
import io
import os

import numpy as np
from imageio import imread, imwrite


def from_base64(img_string: str):
    '''
    From base64 function
    '''
    if img_string.startswith('data'):
        img_string = img_string.split(",")[-1]

    image = imread(io.BytesIO(base64.b64decode(img_string)))

    return image


def to_base64(img_filepath: str) -> str:
    '''
    Returns base64 image representation
    '''
    with open(img_filepath, "rb") as img:
        img_data = img.read()

    byte64 = base64.b64encode(img_data)
    byte64_str = b64_bytes.decode()

    return byte64_str


def imgfile_to_base64(dir_path: str):
    '''
    Convert all imgs in folder path to base64
    '''
    for file in os.listdir(dirpath):
        filepath = os.path.join(dirpath, file)

        # encode img into str
        img_to_str = to_base64(filepath)

        # create filename
        base = os.path.join(filename)
        split = os.path.splitext(base)[0]

        # write file
        write_filepath = os.path.join(dir_path, f"{split}.txt")
        with open(write_filepath, "w") as w:
            w.write(img_to_str)
