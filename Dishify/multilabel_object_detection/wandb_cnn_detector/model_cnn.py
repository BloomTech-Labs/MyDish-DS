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

import wandb
from wandb.keras import WandbCallback
import load_dotenv

import os
import pickle


# Set defaults for each parameter
hyperparameter_defaults = dict(
    learning_rate=0.001,
    epochs=5,
    optimizer="adam",
    num_filters=2,
    base_kernel_size=2,
    dropout_rate=0.3,
    loss_function="categorical_crossentropy"
)

wandb.init(config=hyperparameter_defaults)
config = wandb.config

load_dotenv()
WANDB_API_KEY = os.getenv("WANDB_API_KEY")


# Will implement the logic where a dictionary is converted into a pickle file
# Then, the pickle file will be loaded in for training.
# That logic lives in the util folder. Needs to be tuned a little to work with
# this model.
with open('data/Inception_multilabel_detection_model.pkl', 'rb') as f:
    cnn_data = pickle.load(f)


def build_model(num_filters=2, dropout_rate=0.3, base_kernel_size=2):
    """Builds a CNN with hyperparamters.
    param num_filters: Num of filter in each cnn layer
    param droput_rate: Dropout rate of each layer
    param base_kernel_size: Size of stride of first convolutional layer.
                Each additional layer's stride is incremented from this value.

    returns: Instantiated, uncompiled model.
    """
    # Input Layer
    inputs = Input(shape=(MAX_SEQ_LENGTH,))

    # Embedding layer
    embedding_layer = Embedding(input_dim=N_FEATURES + 1,
                                output_dim=EMBEDDINGS_LEN,
                                # pre-trained embeddings
                                weights=[embeddings_index],
                                input_length=MAX_SEQ_LENGTH,
                                trainable=False,
                                )(inputs)
    embedding_dropped = Dropout(dropout_rate)(embedding_layer)

    # Convolution Layer - 3 Convolutions, each connected to input embeddings
    # Branch a
    conv_a = Convolution2D(filters=num_filters,
                           kernel_size=base_kernel_size,
                           activation='relu',
                           )(embedding_dropped)
    pooled_conv_a = MaxPooling2D()(conv_a)
    pooled_conv_dropped_a = Dropout(dropout_rate)(pooled_conv_a)

    # Branch b
    conv_b = Convolution2D(filters=num_filters,
                           kernel_size=base_kernel_size + 1,
                           activation='relu',
                           )(embedding_dropped)
    pooled_conv_b = MaxPooling2D()(conv_b)
    pooled_conv_dropped_b = Dropout(dropout_rate)(pooled_conv_b)

    # Branch c
    conv_c = Convolution2D(filters=num_filters,
                           kernel_size=base_kernel_size + 2,
                           activation='relu',
                           )(embedding_dropped)
    pooled_conv_c = MaxMaxPooling2D()(conv_c)
    pooled_conv_dropped_c = Dropout(dropout_rate)(pooled_conv_c)

    conv_d = Convolution2D(filters=num_filters,
                           kernel_size=base_kernel_size + 3,
                           activation='relu',
                           )(embedding_dropped)

    pooled_conv_d = MaxPooling2D()(conv_d)
    pooled_conv_dropped_d = Dropout(droput_rate)(pooled_conv_d)

    conv_e = Convolution2D(filters=num_filters,
                           kernel_size=base_kernel_size + 4,
                           activation='relu',
                           )(embedding_dropped)

    pooled_conv_e = MaxPooling2D()(conv_e)
    pooled_conv_dropped_e = Dropout(droput_rate)(pooled_conv_e)

    # Collect branches into a single Convolution layer
    concat = Concatenate()(
        [pooled_conv_dropped_a, pooled_conv_dropped_b, pooled_conv_dropped_c,
         pooled_conv_d, pooled_conv_e])
    concat_dropped = Dropout(dropout_rate)(concat)

    # Flatten Layer
    flat = Flatten()(concat_dropped)

    # Dense output layer
    prob = Dense(units=1,  # dimensionality of the output space
                 activation='sigmoid',
                 )(flat)

    return Model(inputs, prob)


model = build_model(config.num_filters, config.dropout_rate,
                    config.base_kernel_size)
model.compile(loss=config.loss_function,
              optimizer=config.optimizer, metrics=['accuracy'])

model.fit(x_train, y_train, batch_size=32,
          steps_per_epoch=len(x_train) / 32, epochs=config.epochs,
          validation_data=(x_val, y_val),
          callbacks=[WandbCallback(validation_data=(x_val, y_val))])
