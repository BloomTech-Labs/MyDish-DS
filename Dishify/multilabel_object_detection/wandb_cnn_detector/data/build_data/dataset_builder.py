
def build_dataset(params):

    if params['REBUILD_DATASET']:  # new dataset instance
        if(params['VERBOSE'] > 0):
            silence = False
            logging.info('Building ' + params['DATASET_NAME'] + ' dataset')
        else:
            silence = True

        base_path = params['DATA_PATH']
        ds = Dataset(params['DATASET_NAME'], base_path +
                     params.get('SUFFIX_DATASET', '/images'), silence=silence)

        # INPUT DATA
        # IMAGES
        ds.setInput(base_path+'/'+params['IMG_FILES']['train'], 'train',
                    type='raw-image', id=params['INPUTS_IDS_DATASET'][0],
                    img_size=params['IMG_SIZE'], img_size_crop=params['IMG_SIZE_CROP'])
        ds.setInput(base_path+'/'+params['IMG_FILES']['val'], 'val',
                    type='raw-image', id=params['INPUTS_IDS_DATASET'][0],
                    img_size=params['IMG_SIZE'], img_size_crop=params['IMG_SIZE_CROP'])
        ds.setInput(base_path+'/'+params['IMG_FILES']['test'], 'test',
                    type='raw-image', id=params['INPUTS_IDS_DATASET'][0],
                    img_size=params['IMG_SIZE'], img_size_crop=params['IMG_SIZE_CROP'])
        # Set train mean
        ds.setTrainMean(
            mean_image=params['MEAN_IMAGE'], data_id=params['INPUTS_IDS_DATASET'][0])

        # OUTPUT DATA
        if params['CLASSIFICATION_TYPE'] == 'single-label':

            # train split
            ds.setOutput(base_path + '/' + params['LABELS_FILES']['train'], 'train',
                         type='categorical', id=params['OUTPUTS_IDS_DATASET'][0])
            # val split
            ds.setOutput(base_path + '/' + params['LABELS_FILES']['val'], 'val',
                         type='categorical', id=params['OUTPUTS_IDS_DATASET'][0])
            # test split
            ds.setOutput(base_path + '/' + params['LABELS_FILES']['test'], 'test',
                         type='categorical', id=params['OUTPUTS_IDS_DATASET'][0])

        elif params['CLASSIFICATION_TYPE'] == 'multi-label':

            # Convert list of ingredients into classes
            logging.info(
                'Preprocessing list of ingredients for assigning vocabulary as image classes.')
            [classes, word2idx, idx2word] = convertIngredientsList2BinaryClasses(base_path,
                                                                                 params['LABELS_FILES'],
                                                                                 params['CLASSES_PATH'],
                                                                                 type_list=params.get('LABELS_TYPE_LIST', 'identifiers'))

            # Insert them as outputs
            ds.setOutput(classes['train'], 'train', type='categorical',
                         id=params['OUTPUTS_IDS_DATASET'][0])
            ds.setOutput(classes['val'], 'val', type='categorical',
                         id=params['OUTPUTS_IDS_DATASET'][0])
            ds.setOutput(classes['test'], 'test', type='categorical',
                         id=params['OUTPUTS_IDS_DATASET'][0])

            # Insert vocabularies
            ds.extra_variables['word2idx_binary'] = word2idx
            ds.extra_variables['idx2word_binary'] = idx2word

            if 'Food_and_Ingredients' in params['DATASET_NAME']:

                # train split
                ds.setOutput(base_path + '/' + params['LABELS_FILES_FOOD']['train'], 'train',
                             type='categorical', id=params['OUTPUTS_IDS_DATASET'][1])
                # val split
                ds.setOutput(base_path + '/' + params['LABELS_FILES_FOOD']['val'], 'val',
                             type='categorical', id=params['OUTPUTS_IDS_DATASET'][1])
                # test split
                ds.setOutput(base_path + '/' + params['LABELS_FILES_FOOD']['test'], 'test',
                             type='categorical', id=params['OUTPUTS_IDS_DATASET'][1])

        # Dataset is downloaded, can be used again by storing in the defined path.
        saveDataset(ds, params['STORE_PATH'])

    else:
        # We can easily recover it with a single line
        ds = loadDataset(params['STORE_PATH'] +
                         '/Dataset_'+params['DATASET_NAME']+'.pkl')

    return ds
