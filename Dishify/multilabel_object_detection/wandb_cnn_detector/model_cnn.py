from keras.utils.np_utils import to_categorical
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input, decode_predictions
from keras.preprocessing import image
from keras.layers import Input
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D, AveragePooling2D
from keras.layers.normalization import BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, TensorBoard, CSVLogger
import keras.backend as K
from keras.optimizers import SGD, RMSprop, Adam
from tensorflow.keras.callbacks import EarlyStopping

from config_cnn import load_params
import wandb
from wandb.keras import WandbCallback
import load_dotenv

import os
import pickle


# Set defaults for each parameter
hyperparameter_defaults = dict(
    learning_rate=0.001,
    epochs=10,
    batch_size=5,
    optimizer="adam",
    num_filters=2,
    base_kernel_size=2,
    dropout_rate=0.3,
    loss_function="categorical_crossentropy"
)

wandb.init(project="mydish", config=hyperparameter_defaults)
config = wandb.config

load_dotenv()
WANDB_API_KEY = os.getenv("WANDB_API_KEY")


# Will implement the logic where a dictionary is converted into a pickle file
# Then, the pickle file will be loaded in for training.
# That logic lives in the util folder. Needs to be tuned a little to work with
# this model.
with open('data/Dataset_Food_Recipes5k_complete.pkl', 'rb') as f:
    cnn_data = pickle.load(f)

train_labels = 'data/images/Recipes5k/annotations/train_labels.txt'
val_labels = 'data/images/Recipes5k/annotations/val_labels.txt'
classes_labels = 'data/images/Recipes5k/annotations/classes_Recipes5k.txt'
ingred_labels = 'data/images/Recipes5k/annotations/ingredients_Recipes5k'

# number of classes
num_classes = len(classes_labels)

# train/val
(x_train, y_train), (x_val, y_val) = cnn_data

# normalize data
x_train = x_train.astype('float32') / 255.
x_val = x_val.astype('float32') / 255.


def build_model(num_filters=2, dropout_rate=0.3, base_kernel_size=2):
    """Builds a CNN with hyperparamters.
    param num_filters: Num of filter in each cnn layer
    param droput_rate: Dropout rate of each layer
    param base_kernel_size: Size of stride of first convolutional layer.
                Each additional layer's stride is incremented from this value.

    returns: Instantiated, uncompiled model.
    """
    # Input Layer
    inputs = Input(shape=(params['INPUTS_IDS_MODEL']))

    # Convolution2D layers
    conv1 = Conv2D(64, (3, 3), activation='relu',
                   padding='same', name='conv1_1')(inputs)

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

    conv6 = Conv2D(256, (3, 3), activation='relu',
                   padding='same')(up_conv5)
    conv6 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv6)
    conv6 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv6)

    up_conv6 = UpSampling2D(size=(2, 2))(conv6)
    up_conv6 = ZeroPadding2D()(up_conv6)

    conv7 = Conv2D(128, (3, 3), activation='relu',
                   padding='same')(up_conv6)
    conv7 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv7)
    conv7 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv7)

    up_conv7 = UpSampling2D(size=(2, 2))(conv7)
    up_conv7 = ZeroPadding2D()(up_conv7)

    conv8 = Conv2D(128, (3, 3), activation='relu',
                   padding='same')(up_conv7)
    conv8 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv8)
    conv8 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv8)

    up_conv8 = UpSampling2D(size=(2, 2))(conv8)
    up_conv8 = ZeroPadding2D()(up_conv8)

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

    return Model(inputs, out)


model = build_model(config.num_filters, config.dropout_rate,
                    config.base_kernel_size)
model.compile(loss=config.loss_function,
              optimizer=config.optimizer, metrics=['categorical_accuracy'])

# log the number of total parameters
config.total_params = model.count_params()
print("Total params: ", config.total_params)

model.fit(x_train, y_train, batch_size=32,
          steps_per_epoch=len(x_train) / 32, epochs=config.epochs,
          validation_data=(x_val, y_val),
          callbacks=[WandbCallback(validation_data=(x_val, y_val),
                                   labels=[train_labels, classes_labels]))])
