import logging
import numpy as np
from timeit import default_timer as timer
import copy
import sys

from keras_wrapper.cnn_model import saveModel, loadModel
from keras_wrapper.extra import evaluation
from keras_wrapper.extra.callbacks import EvalPerformance
from keras_wrapper.extra.read_write import *
from keras_wrapper.utils import decode_multilabel

from exploratory.data_configs.prep_data import build_dataset
from config import load_params
from model import Ingredients_Model

'''
Logic for running predictions on a previously trained model.

'''


def apply_model(params):
    """
        Function for using a previously trained model for predicting.
    """

    # Load data
    dataset = build_dataset(params)
    ###########

    # Load model
    ing_model = loadModel(params['STORE_PATH'], params['RELOAD'])
    ing_model.setOptimizer()
    ###########

    # Apply sampling
    callbacks = buildCallbacks(params, ing_model, dataset)
    callbacks[0].evaluate(params['RELOAD'], 'epoch')

    for s in params["EVAL_ON_SETS"]:
        # Apply model predictions
        params_prediction = {'batch_size': params['BATCH_SIZE'], 'n_parallel_loaders': params['PARALLEL_LOADERS'],
                             'predict_on_sets': [s], 'normalize': params['NORMALIZE_IMAGES'],
                             'mean_substraction': params['MEAN_SUBSTRACTION']}
        predictions = ing_model.predictNet(dataset, params_prediction)[s]

        # Format predictions
        predictions = decode_multilabel(predictions,  # not used
                                        dataset.extra_variables['idx2word_binary'],
                                        min_val=params['MIN_PRED_VAL'], verbose=1)

        # Store result
        filepath = ing_model.model_path+'/' + s + '_labels.pred'  # results file
        listoflists2file(filepath, predictions)

        # Evaluate result
        extra_vars = dict()
        extra_vars[s] = dict()
        extra_vars[s]['word2idx'] = dataset.extra_variables['word2idx_binary']
        exec("extra_vars[s]['references'] = dataset.Y_" +
             s+"[params['OUTPUTS_IDS_DATASET'][0]]")
        for metric in params['METRICS']:
            logging.info('Evaluating on metric ' + metric)
            # Evaluate on the chosen metric
            metrics = evaluation.select[metric](
                pred_list=predictions,
                verbose=1,
                extra_vars=extra_vars,
                split=s)


if __name__ == "__main__":

    cf = 'config'
    for arg in sys.argv[1:]:
        k, v = arg.split('=')
        if k == 'config_file':
            cf = v
    cf = __import__(cf)
    params = cf.load_params()

    if(params['MODE'] == 'predict'):
        logging.info('Running predict.')
        apply_model(params)

    logging.info('Done!')
