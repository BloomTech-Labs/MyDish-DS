# keras Imports
import keras
from keras.engine import Input
from keras.layers.core import Dropout, RepeatVector, Dense, Flatten, Activation, Lambda
from keras.layers.embeddings import Embedding
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D, AveragePooling2D, GlobalMaxPooling2D, Cropping2D
from keras.layers import Concatenate as Concat
from keras.layers.recurrent import LSTM
from keras.models import model_from_json, Sequential, Model
from keras.layers.advanced_activations import PReLU
from keras.layers.normalization import BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.layers import Flatten, Permute
from keras.layers import Convolution2D as Conv2D
from keras.layers.convolutional import UpSampling2D


# Model imports(ResNet50, InceptionV3, VGG16) # NOTE: no current config for VGG16 in the config file.
from keras.applications.resnet50 import ResNet50
from keras.applications.vgg16 import VGG16
from keras.applications.inception_v3 import InceptionV3

import tensorflow as tf
import keras
# custom keras import
from keras_wrapper.cnn_model import Model_Wrapper

import numpy as np
import os
import logging
import shutil
import time
import copy

"""
NOTE: Configurations of the models params are in config.py, to change the params
      do so in the config file.
"""


class Ingredients_Model(Model_Wrapper):

    def __init__(self, params, type='Inception', verbose=1, structure_path=None, weights_path=None,
                 model_name=None, store_path=None, seq_to_functional=False):
        """
            Ingredients_Model object constructor.

            :param params: all hyperparameters of the model.
            :param type: network name type (corresponds to any method defined in the section 'MODELS' of this class). Only valid if 'structure_path' == None.
            :param verbose: set to 0 if you don't want the model to output informative messages
            :param structure_path: path to a Keras' model json file. If we speficy this parameter then 'type' will be only an informative parameter.
            :param weights_path: path to the pre-trained weights file (if None, then it will be randomly initialized)
            :param model_name: optional name given to the network (if None, then it will be assigned to current time as its name)
            :param store_path: path to the folder where the temporal model packups will be stored
            :param seq_to_functional: defines if we are loading a set of weights from a Sequential model to a FunctionalAPI model (only applicable if weights_path is not None)
        """
        super(self.__class__, self).__init__(model_name=model_name,
                                             silence=verbose, inheritance=True)

        self.__toprint = ['_model_type', 'name', 'model_path', 'verbose']

        self.verbose = verbose
        self._model_type = type
        self.params = params

        # Sets the model name and prepares the folders for storing the models
        self.setName(model_name, store_path)

        # Prepare model
        if structure_path:
            # Load a .json model
            if self.verbose > 0:
                logging.info(
                    "<<< Loading model structure from file " + structure_path + " >>>")
            self.model = model_from_json(open(structure_path).read())
        else:
            # Build model from scratch
            if hasattr(self, type):
                if self.verbose > 0:
                    logging.info("<<< Building " + type +
                                 " Ingredients_Model >>>")
                eval('self.'+type+'(params)')
            else:
                raise Exception('Ingredients_Model type "' +
                                type + '" is not implemented.')

        # Load weights from file
        if weights_path:
            if self.verbose > 0:
                logging.info("<<< Loading weights from file " +
                             weights_path + " >>>")
            self.model.load_weights(
                weights_path, seq_to_functional=seq_to_functional)

        # Print information of self
        if verbose > 0:
            print(self.verbose)
            self.model.summary()

     #   self.setOptimizer()

    def setOptimizer(self, lr=0.001, loss='categorical_crossentropy', optimizer='adam'):
        """
            Sets a new optimizer for the model.
        """

        super(self.__class__, self).setOptimizer(lr=self.params['LR'],
                                                 loss=self.params['LOSS'],
                                                 optimizer=self.params['OPTIMIZER'],
                                                 momentum=self.params['MOMENTUM'],
                                                 loss_weights=self.params.get(
                                                     'LOSS_WIGHTS', None),
                                                 sample_weight_mode='temporal' if self.params.get('SAMPLE_WEIGHTS', False) else None)

    def setName(self, model_name, store_path=None, clear_dirs=True):
        """
            Changes the name (identifier) of the model instance.
        """
        if model_name is None:
            self.name = time.strftime("%Y-%m-%d") + '_' + time.strftime("%X")
            create_dirs = False
        else:
            self.name = model_name
            create_dirs = True

        if store_path is None:
            self.model_path = 'Models/' + self.name
        else:
            self.model_path = store_path

        # Remove directories if existed
        if clear_dirs:
            if os.path.isdir(self.model_path):
                shutil.rmtree(self.model_path)

        # Create new ones
        if create_dirs:
            if not os.path.isdir(self.model_path):
                os.makedirs(self.model_path)

    def decode_predictions(self, preds, temperature, index2word, sampling_type=None, verbose=0):
        """
        Decodes predictions
        In:
            preds - predictions codified as the output of a softmax activiation function
            temperature - temperature for sampling (not used for this model)
            index2word - mapping from word indices into word characters
            sampling_type - sampling type (not used for this model)
            verbose - verbosity level, by default 0
        Out:
            Answer predictions (list of answers)
        """
        labels_pred = np.where(np.array(preds) > 0.5, 1, 0)
        labels_pred = [[index2word[e] for e in np.where(
            labels_pred[i] == 1)[0]] for i in range(labels_pred.shape[0])]
        return labels_pred

    #  VISUALIZATION Methods for visualization

    def __str__(self):
        """
            Plot basic model information.
        """
        obj_str = '-----------------------------------------------------------------------------------\n'
        class_name = self.__class__.__name__
        obj_str += '\t\t'+class_name + ' instance\n'
        obj_str += '-----------------------------------------------------------------------------------\n'

        # Print pickled attributes
        for att in self.__toprint:
            obj_str += att + ': ' + str(self.__dict__[att])
            obj_str += '\n'

        obj_str += '\n'
        obj_str += 'MODEL PARAMETERS:\n'
        obj_str += str(self.params)
        obj_str += '\n'

        obj_str += '-----------------------------------------------------------------------------------'

        return obj_str

    #   PREDEFINED MODELS

    def VGG16(self, params):

        self.ids_inputs = params["INPUTS_IDS_MODEL"]
        self.ids_outputs = params["OUTPUTS_IDS_MODEL"]

        activation_type = params['CLASSIFIER_ACTIVATION']
        nOutput = params['NUM_CLASSES']

        # Load VGG16 model pre-trained on ImageNet

        self.model = VGG16(weights='imagenet',
                           layers_lr=params['PRE_TRAINED_LR_MULTIPLIER'],
                           input_name=self.ids_inputs[0])

        # Recover input layer
        image = self.model.get_layer(self.ids_inputs[0]).output

        # Recover last layer kept from original model: 'fc2'
        x = self.model.get_layer('fc2').output

        # Create last layer (classification)

        x = Dense(nOutput, activation=activation_type, name=self.ids_outputs[0],
                  W_learning_rate_multiplier=params['NEW_LAST_LR_MULTIPLIER'],
                  b_learning_rate_multiplier=params['NEW_LAST_LR_MULTIPLIER'])(x)

        self.model = Model(input=image, output=x)
        self.model.compile(optimizer='adam', loss='categorical_crossentropy')

    def Inception(self, params):

        self.ids_inputs = params["INPUTS_IDS_MODEL"]
        self.ids_outputs = params["OUTPUTS_IDS_MODEL"]

        activation_type = params['CLASSIFIER_ACTIVATION']
        nOutput = params['NUM_CLASSES']

        # Load Inception model pre-trained on ImageNet

        self.model = InceptionV3(weights='imagenet')

        # Freeze the base model
    #    self.model.trainable = False

        # Recover input layer
        image = self.model.get_layer(self.ids_inputs[0]).output

        # Convolution2D layers
        conv1 = Conv2D(64, (3, 3), activation='relu',
                       padding='same', name='conv1_1')(image)

        conv1 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv1)
        conv1 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv1)
        pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

        conv2 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool1)
        conv2 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv2)
        conv2 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv2)
        pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

        conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool2)
        conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv3)
        conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv3)
        pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

        conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(pool3)
        conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv4)
        conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv4)
        pool4 = MaxPooling2D(pool_size=(2, 2))(conv4)

        # Middle of the path (bottleneck)
        conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(pool4)
        conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(conv5)
        conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(conv5)

        # Upsampling path
        up_conv5 = UpSampling2D(size=(2, 2))(conv5)
        up_conv5 = ZeroPadding2D()(up_conv5)
   #     up6 = Concat(cropping=[None, None, 'center', 'center'])([conv4, up_conv5])
        conv6 = Conv2D(256, (3, 3), activation='relu',
                       padding='same')(up_conv5)
        conv6 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv6)
        conv6 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv6)

        up_conv6 = UpSampling2D(size=(2, 2))(conv6)
        up_conv6 = ZeroPadding2D()(up_conv6)
   #     up7 = Concat(cropping=[None, None, 'center', 'center'])([conv3, up_conv6])
        conv7 = Conv2D(128, (3, 3), activation='relu',
                       padding='same')(up_conv6)
        conv7 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv7)
        conv7 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv7)

        up_conv7 = UpSampling2D(size=(2, 2))(conv7)
        up_conv7 = ZeroPadding2D()(up_conv7)
  #      up8 = Concat(cropping=[None, None, 'center', 'center'])([conv2, up_conv7])
        conv8 = Conv2D(128, (3, 3), activation='relu',
                       padding='same')(up_conv7)
        conv8 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv8)
        conv8 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv8)

        up_conv8 = UpSampling2D(size=(2, 2))(conv8)
        up_conv8 = ZeroPadding2D()(up_conv8)
   #     up9 = Concat(cropping=[None, None, 'center', 'center'])([conv1, up_conv8])
        conv9 = Conv2D(64, (3, 3), activation='relu', padding='same')(up_conv8)
        conv9 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv9)
        conv9 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv9)

        # Final classification layer (batch_size, classes, width, height)
        x = Conv2D(params['NUM_CLASSES'], (1, 1), border_mode='same')(conv9)

        # Create last layer (classification)
        x = Dense(nOutput, activation=activation_type)(x)

        x = Dense(2000, activation='tanh')(x)

        x = Dense(1000, activation='tanh')(x)

        x = Dense(500, activation='tanh')(x)

        # output
        out = Activation(params['CLASSIFIER_ACTIVATION'],
                         name=self.ids_outputs[0])(x)

        # instantiate model
        self.model = Model(inputs=image, outputs=out)

        # compile
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=[
                           'categorical_accuracy'])

        # summary
        self.model.summary()

    def ResNet50(self, params):

        self.ids_inputs = params["INPUTS_IDS_MODEL"]
        self.ids_outputs = params["OUTPUTS_IDS_MODEL"]

        activation_type = params['CLASSIFIER_ACTIVATION']
        nOutput = params['NUM_CLASSES']

        # Load ResNet50 model pre-trained on ImageNet
        self.model = ResNet50(weights='imagenet')

        # Recover input layer
        image = self.model.get_layer(self.ids_inputs[0]).output

        # Convolution2D layers
        conv1 = Conv2D(64, (3, 3), activation='relu',
                       padding='same', name='conv1_1')(image)

        conv1 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv1)
        conv1 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv1)
        pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

        conv2 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool1)
        conv2 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv2)
        conv2 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv2)
        pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

        conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool2)
        conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv3)
        conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv3)
        pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

        conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(pool3)
        conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv4)
        conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv4)
        pool4 = MaxPooling2D(pool_size=(2, 2))(conv4)

        # Middle of the path (bottleneck)
        conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(pool4)
        conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(conv5)
        conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(conv5)

        # Final classification layer (batch_size, classes, width, height)
        x = Conv2D(params['NUM_CLASSES'], (1, 1), border_mode='same')(conv5)

        # Create last layer (classification)
        x = Dense(500, activation='tanh')(x)

        x = Dense(1000, activation='tanh')(x)

        x = Dense(2000, activation='tanh')(x)

        x = Dense(nOutput, activation=activation_type)(x)

        # output
        out = Activation(params['CLASSIFIER_ACTIVATION'],
                         name=self.ids_outputs[0])(x)

        # instantiate model
        self.model = Model(inputs=image, outputs=out)

        # compile
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=[
                           'categorical_accuracy'])

        # summary
        self.model.summary()

    def TestModel(self, params):

        self.ids_inputs = params["INPUTS_IDS_MODEL"]
        self.ids_outputs = params["OUTPUTS_IDS_MODEL"]

        activation_type = params['CLASSIFIER_ACTIVATION']
        nOutput = params['NUM_CLASSES']

        # Load ResNet50 model pre-trained on ImageNet
        self.model = ResNet50(weights='imagenet',
                              layers_lr=params['PRE_TRAINED_LR_MULTIPLIER'],
                              input_shape=tuple(
                                  [params['IMG_SIZE_CROP'][2]] + params['IMG_SIZE_CROP'][:2]),
                              include_top=False, input_name=self.ids_inputs[0])

        # Recover input layer
        image = self.model.get_layer(self.ids_inputs[0]).output

        # Create last layer (classification)
        x = Flatten()(image)
        x = Dense(nOutput, activation=activation_type, name=self.ids_outputs[0],
                  W_learning_rate_multiplier=params['NEW_LAST_LR_MULTIPLIER'],
                  b_learning_rate_multiplier=params['NEW_LAST_LR_MULTIPLIER'])(x)

        self.model = Model(input=image, output=x)

        self.model.compile(optimizer='adam', loss='categorical_crossentropy')

    # Auxiliary functions
    def changeClassifier(self, params, last_layer='flatten'):

        self.ids_inputs = params["INPUTS_IDS_MODEL"]
        self.ids_outputs = params["OUTPUTS_IDS_MODEL"]

        activation_type = params['CLASSIFIER_ACTIVATION']

        ########
        inp = self.model.get_layer(self.ids_inputs[0]).output

        last = self.model.get_layer(last_layer).output

        out = Dense(params['NUM_CLASSES'], activation=activation_type, name=self.ids_outputs[0],
                    W_learning_rate_multiplier=params['NEW_LAST_LR_MULTIPLIER'],
                    b_learning_rate_multiplier=params['NEW_LAST_LR_MULTIPLIER'])(last)

        self.model = Model(input=inp, output=out)

        self.model.compile(optimizer='adam', loss='categorical_crossentropy')
