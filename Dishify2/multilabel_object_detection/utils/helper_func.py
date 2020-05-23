import io
import os
import glob
import csv

import math
import numpy as np
from imageio import imread, imwrite

import tensorflow as tf
import skimage.io
import skimage.transform
import skimage.filters

from matplotlib import pyplot
from matplotlib.image import imread

'''
An assortment of helpful functions
'''


def print_organizer(printer_split):
    '''
    In the terminal, this function will help organize
    the print statements.
    '''
    line = '-'*min(10, len(printer_split))
    print(line + '' + printer_split + '' + line)


def txt_to_csv(directory, output):
    '''
    Converts txt files to csv
    '''

    txt_files = os.path.join(directory, '*.txt')

    for txt_file in glob.glob(txt_files):
        with open(txt_file, "rb") as input_file:
            in_txt = csv.reader(input_file, delimiter='=')
            filename = os.path.splitext(os.path.basename(txt_file))[0] + '.csv'

            with open(os.path.join(output, filename), 'wb') as output_file:
                writer = out_csv = csv.writer(output_file)
                rows = out_csv.writerows(in_txt)

            return writer, rows


def plot_folder_img(folder, file):
    '''
    Plot the images stored in your path

    folder = Path to folder containing the images
    file = name of of the image

    Note: You can plot multiple imgs.
    '''
    for i in range(4):
        #  subplot
        pyplot.subplot(330 + 1 + i)
        #  filename
        filename = folder + str(i) + f'{file}' + '.jpg'
        # load image pixels
        image = imread(filename)
        # plot raw pixel data
        img = pyplot.imshow(image)
        # show the figure
        plot = pyplot.show()

        return img, plot


def tensor_summary(tensor):
    """Display shape, min, and max values of a tensor."""
    print("shape: {}  min: {}  max: {}".format(
        tensor.shape, tensor.min(), tensor.max()))


def normalize(image):
    """Takes a tensor of 3 dimensions (height, width, colors) and normalizes it's values
    to be between 0 and 1 so it's suitable for displaying as an image."""
    image = image.astype(np.float32)
    return (image - image.min()) / (image.max() - image.min() + 1e-5)


def display_images(images, titles=None, cols=5, interpolation=None, cmap="Greys_r"):
    """
    images: A list of images. It can be either:
        - A list of Numpy arrays. Each array represents an image.
        - A list of lists of Numpy arrays. In this case, the images in
          the inner lists are concatentated to make one image.
    """
    titles = titles or [""] * len(images)
    rows = math.ceil(len(images) / cols)
    height_ratio = 1.2 * (rows/cols) * \
        (0.5 if type(images[0]) is not np.ndarray else 1)
    plt.figure(figsize=(15, 15 * height_ratio))
    i = 1
    for image, title in zip(images, titles):
        plt.subplot(rows, cols, i)
        plt.axis("off")
        # Is image a list? If so, merge them into one image.
        if type(image) is not np.ndarray:
            image = [normalize(g) for g in image]
            image = np.concatenate(image, axis=1)
        else:
            image = normalize(image)
        plt.title(title, fontsize=9)
        plt.imshow(image, cmap=cmap, interpolation=interpolation)
        i += 1
