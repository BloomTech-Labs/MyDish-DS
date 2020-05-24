import io
import os
import glob
import csv
import logging
import sys
import tables
import json
from __future__ import print_function
from six import iteritems
import codecs
import pickle as pk

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

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)


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

    directory: Directory containing all your txt files.
    output: Conversion to csv output is stored in the defined path you give it.
    '''

    txt_files = os.path.join(directory, '*.txt')

    for txt_file in glob.glob(txt_files):
        with open(txt_file, "rb") as input_file:
            in_txt = csv.reader(input_file, delimiter='=')
            filename = os.path.splitext(os.path.basename(txt_file))[0] + '.csv'

            with open(os.path.join(output, filename), 'wb') as output_file:
                out_csv = csv.writer(output_file)
                writer = out_csv.writerows(in_txt)

            return writer


def txt_to_csv2(txtfile, csvfile):
    '''
    Another function that converts txt files to csv.

    txtfile: can be directory or a singular text file
    csvfile: Conversion to csv output is stored in the defined path you give it.
    '''
    with open(txtfile, 'r') as infile, open(csvfile, 'w') as outfile:
        stripped = (line.strip() for line in infile)
        lines = (line.split(",") for line in stripped if line)
        out_csv = csv.writer(outfile)
        writer = writer.writerows(lines)

        return writer


def plot_folder_img(folder, file):
    '''
    Plot the images stored in your path

    folder: Path to folder containing the images
    file: name of of the image

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


def tensor_normalize(image):
    """Takes a tensor of 3 dimensions (height, width, colors) and normalizes it's values
    to be between 0 and 1 so it's suitable for displaying as an image."""
    image = image.astype(np.float32)
    return (image - image.min()) / (image.max() - image.min() + 1e-5)


def tensor_display_images(images, titles=None, cols=5, interpolation=None, cmap="Greys_r"):
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


def create_dir_if_not_exists(directory):
    """
    Creates a directory if it doen't exist
    :param directory: Directory to create
    :return: None
    """
    if not os.path.exists(directory):
        logger.info("<<< creating directory " + directory + " ... >>>")
        os.makedirs(directory)


def clean_dir(directory):
    """
    Creates (or empties) a directory
    :param directory: Directory to create
    :return: None
    """

    if os.path.exists(directory):
        import shutil
        logger.warning('<<< Deleting directory: %s >>>' % directory)
        shutil.rmtree(directory)
        os.makedirs(directory)
    else:
        os.makedirs(directory)


# Main functions
def file2list(filepath,
              stripfile=True):
    """
    Loads a file into a list. One line per element.
    :param filepath: Path to the file to load.
    :param stripfile: Whether we should strip the lines of the file or not.
    :return: List containing the lines read.
    """
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        lines = [k for k in [k.strip() for k in f.readlines()] if len(k) > 0] if stripfile else [k for k in
                                                                                                 f.readlines()]
        return lines


def numpy2file(filepath,
               mylist,
               permission='wb',
               split=False):
    """
    Saves a numpy array as a file.
    :param filepath: Destination path.
    :param mylist: Numpy array to save.
    :param permission: Write permission.
    :param split: Whether we save each element from mylist in a separate file or not.
    :return:
    """
    mylist = np.asarray(mylist)
    if split:
        for i, filepath_ in list(enumerate(filepath)):
            with open(filepath_, permission) as f:
                np.save(f, mylist[i])
    else:
        with open(filepath, permission) as f:
            np.save(f, mylist)


def numpy2imgs(folder_path,
               mylist,
               imgs_names,
               dataset):
    """
    Save a numpy array as images.
    :param folder_path: Folder of the images to save.
    :param mylist: Numpy array containing the images.
    :param imgs_names: Names of the images to be saved.
    :param dataset:
    :return:
    """
    from PIL import Image as pilimage
    create_dir_if_not_exists(folder_path)
    n_classes = mylist.shape[-1]

    for img, name in zip(mylist, imgs_names):
        name = '_'.join(name.split('/'))
        file_path = folder_path + "/" + name  # image file

        out_img = dataset.getImageFromPrediction_3DSemanticLabel(
            img, n_classes)

        # save the segmented image
        out_img = pilimage.fromarray(np.uint8(out_img))
        out_img.save(file_path)


def listoflists2file(filepath,
                     mylist,
                     permission='w'):
    """
    Saves a list of lists into a file. Each element in a line.
    :param filepath: Destination file.
    :param mylist: List of lists to save.
    :param permission: Writing permission.
    :return:
    """
    mylist = [encode_list(sublist) for sublist in mylist]
    mylist = [item for sublist in mylist for item in sublist]
    mylist = u'\n'.join(mylist)
    with codecs.open(filepath, permission, encoding='utf-8') as f:
        f.write(mylist)
        f.write('\n')


def list2file(filepath,
              mylist,
              permission='w'):
    """
    Saves a list into a file. Each element in a line.
    :param filepath: Destination file.
    :param mylist: List to save.
    :param permission: Writing permission.
    :return:
    """
    mylist = encode_list(mylist)
    mylist = u'\n'.join(mylist)
    with codecs.open(filepath,
                     permission,
                     encoding='utf-8') as f:
        f.write(mylist)
        f.write('\n')


def list2stdout(mylist):
    """
    Prints a list in STDOUT
    :param mylist: List to print.
    """
    mylist = encode_list(mylist)
    mylist = '\n'.join(mylist)
    print(mylist)


def dump_hdf5_simple(filepath,
                     dataset_name,
                     data):
    """
    Saves a HDF5 file.
    """
    import h5py
    h5f = h5py.File(filepath,
                    'w')
    h5f.create_dataset(dataset_name,
                       data=data)
    h5f.close()


def load_hdf5_simple(filepath,
                     dataset_name='data'):
    """
    Loads a HDF5 file.
    """
    import h5py
    h5f = h5py.File(filepath, 'r')
    tmp = h5f[dataset_name][:]
    h5f.close()
    return tmp


def model_to_json(path,
                  model):
    """
    Saves model as a json file under the path.
    """
    json_model = model.to_json()
    with open(path, 'w') as f:
        json.dump(json_model, f)


def json_to_model(path):
    """
    Loads a model from the json file.
    """
    from keras.models import model_from_json
    with open(path, 'r') as f:
        json_model = json.load(f)
    model = model_from_json(json_model)
    return model


def dict2file(mydict,
              path,
              title=None,
              separator=':',
              permission='a'):
    """
    In:
        mydict - dictionary to save in a file
        path - path where mydict is stored
        title - the first sentence in the file;
            useful if we write many dictionaries
            into the same file
    """
    tmp = [encode_list([x[0]])[0] + separator + encode_list([x[1]])[0]
           for x in list(iteritems(mydict))]
    if title is not None:
        output_list = [title]
        output_list.extend(tmp)
    else:
        output_list = tmp
    list2file(path,
              output_list,
              permission=permission)


def dict2pkl(mydict,
             path):
    """
    Saves a dictionary object into a pkl file.
    :param mydict: dictionary to save in a file
    :param path: path where my_dict is stored
    :return:
    """
    if path[-4:] == '.pkl':
        extension = ''
    else:
        extension = '.pkl'
    with open(path + extension, 'wb') as f:
        pk.dump(mydict,
                f,
                protocol=-1)


def pkl2dict(path):
    """
    Loads a dictionary object from a pkl file.
    :param path: Path to the pkl file to load
    :return: Dict() containing the loaded pkl
    """
    with open(path, 'rb') as f:
        if sys.version_info.major == 2:
            return pk.load(f)
        else:
            return pk.load(f,
                           encoding='utf-8')
