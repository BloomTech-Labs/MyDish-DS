"""
File with the parameter configurations.

Params for InceptionV3 also included.

Params for the ResNet50 with customed trained data sourced from http://www.ub.edu/cvub/dataset/
"""


def load_params():
    '''
    Function with params configuration for data path, dataset used config, train,val,test split,
        resizing config, model config, optimizer config, and data storage config.
    '''
    DATA_PATH = 'exploratory/data/image/Recipes5k/'  # path to get data
    # this is a multi-label classification.
    CLASSIFICATION_TYPE = 'multi-label'
    INGREDIENTS_TYPE = 'complete'  # data being used is the complete version

    if CLASSIFICATION_TYPE == 'multi-label':
        if 'Recipes5k' in DATA_PATH:
            if INGREDIENTS_TYPE == 'simplified':
                DATASET_NAME = 'Food_Recipes5k_simplified'
                NUM_CLASSES = 1013  # num of label/classes in the dataset
                CLASSES_PATH = 'annotations/ingredients_simplified_Recipes5k'

                IMG_FILES = {'train': 'annotations/train_images.txt',
                             'val': 'annotations/val_images.txt',
                             'test': 'annotations/test_images.txt'
                             }

                LABEL_FILES = {'train': 'annotations/train_labels.txt',
                               'val': 'annotations/val_labels.txt',
                               'test': 'annotations/test_labels.txt'
                               }

            elif INGREDIENTS_TYPE == 'complete':
                DATASET_NAME = 'Food_Recipes5k_complete'
                NUM_CLASSES = 3213  # num of label/classes in the dataset
                CLASSES_PATH = 'annotations/ingredients_Recipes5k'

                IMG_FILES = {'train': 'annotations/train_images.txt',
                             'val': 'annotations/val_images.txt',
                             'test': 'annotations/test_images.txt'
                             }

                LABEL_FILES = {'train': 'annotations/train_labels.txt',
                               'val': 'annotations/val_labels.txt',
                               'test': 'annotations/test_labels.txt'
                               }

        # metric used to eval after each epoch
        METRICS = ['multilabel_metrics']
        STOP_METRIC = 'f1'
        MIN_PRED_VAL = 0.5

        CLASSIFIER_ACTIVATION = 'sigmoid'  # activation function
        LOSS = 'binary_crossentropy'

    # config for multiple pre-trained(Res,Inception,etc.)
    NETWORK_TYPE = 'ResNet50'

    if NETWORK_TYPE == 'ResNet50':
        # ResNet50
        IMG_SIZE = [256, 256, 3]  # resize image
        IMG_SIZE_CROP = [224, 224, 3]  # input size of network
        INPUTS_IDS_MODEL = ['image']  # corresponding inputs of the built model

        INPUTS_MAPPING = {'image': 0}

    elif NETWORK_TYPE == 'Inception':
        # InceptionV3
        IMG_SIZE = [342, 342, 3]  # resize image
        IMG_SIZE_CROP = [299, 299, 3]  # input size of network
        # corresponding inputs of the built model
        INPUTS_IDS_MODEL = ['input_1']

        INPUTS_MAPPING = {'input_1': 0}

    # Params for the dataset
    INPUTS_IDS_DATASET = ['image']  # corresponding inputs of the dataset
    INPUTS_IDS_MODEL = ['ingredients']  # corresponding inputs of the model
    OUTPUTS_MAPPING = {'ingredients': 0}

    # image mean on the RGB channels of the training data
    MEAN_IMAGE = [104.0067, 116.6690, 122.6795]

    # Image pre-processing params
    NORMALIZE_IMAGES = False
    MEAN_SUBTRACTION = True
    DATA_AUGMENTATION = True  # for training data only

    # Eval params
    EVAL_ON_SETS = ['val', 'test']  # can eval on training too
    START_EVAL_ON_EPOCH = 1  # begins to eval on the first epoch

    # Optimizer params
    OPTIMIZER = 'adam'  # optimizer
    # num of minimum num of epochs before the next LR decay(None=disable)
    LR_DECAY = 1
    LR_GAMMA = 0.9  # multiplier used for decreasing the LR
    LR = 0.001  # LR stands for Learning Rate. really important config that relates to gradient descent

    # extra optimizer params
    PRE_TRAINED_LR_MULTIPLIER = None  # multiplier for a pre-trained network
    # LR multiplier for newly added layers(LR X NEW_LAST_LR_MULTIPLIER)
    NEW_LAST_LR_MULTIPLIER = 1.0

    # Training Params
    # stops when computed this num of epochs. config this as needed.
    MAX_EPOCHS = 100
    # num of epochs to wait to obtain higher accuracy. config as needed.
    PATIENCE = 15
    # num of training utilized per iteration. config as needed.
    BATCH_SIZE = 10
    PARELLEL_LOADERS = 8  # parallel data batch loader
    EPOCHS_FOR_SAVE = 1  # number of epochs between model save
    WRIET_VALID_SAMPLES = True  # write valid samples in file

    # NOTE: Use configured params as needed, change or dont use them. Consider them the defaults.

    # Model Parameters
    # Model used to create first trained model.
    MODEL_TYPE = NETWORK_TYPE = 'ResNet50'

    # Resluts plot and customed model storing params
    # custom name assigned to the model.
    EXTRA_NAME = 'Custom_Recipes5k_complete'
    MODEL_NAME = MODEL_TYPE+'_'+EXTRA_NAME  # model

    # Extra params for Model Parameters
    # None=default. # reuse a previously trianed model with new data.
    REUSE_MODEL_NAME = None
    LAST_LAYER = 'flatten'  # last layer classifcation
    REUSE_MODEL_LOAD = 68

    VERBOSE = 1  # Verbosity
    REBUILD_DATASET = True  # Build Again(True), use stored instance(False)

    # 'training' or 'predict' (if 'predict' then RELOAD must be greater than 0 and EVAL_ON_SETS will be used)
    MODE = 'training'
    RELOAD = 9  # If 0 start training from scratch, otherwise the model saved on epoch 'RELOAD' will be used

    STORE_PATH = 'trained_models/'+MODEL_NAME  # model and eval results

    parameters = locals().copy()
    return parameters
