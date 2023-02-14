'''
Usage: python cnn_test.py {file to load} {save results}
'''

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # don't show all the tensorflow startup messages
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import models
from keras.utils import to_categorical
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import pandas as pd
from sys import path
import h5py


# get the length for the dataset, used for generator function and to calculate steps_per_epoch
def get_dset_len(path, dset):
    with h5py.File(path, 'r') as f:
        return f[dset].shape[0]


# generator function
def generator(dataset_name, batch_size, num_examples):
    with h5py.File(f'processed/DCT_test_{dataset_name}.h5', 'r') as f:
        X = f['DCT']
        while True:
            for i in range(0, num_examples, batch_size):
                batch_X = X[i: min(i + batch_size, num_examples)]
                yield (batch_X)


def get_labels(dataset_name):
    with h5py.File(f'processed/labels_test_{dataset_name}.h5', 'r') as f:
        return np.array(f['labels'][()])


# get predictions and convert numerical values to class name
def get_predictions(dataset_name, model, num_examples):
    predictions = np.argmax(model.predict(
        generator(dataset_name, 32, num_examples), steps=np.ceil(num_examples/32)), axis=1)

    return np.select(
        [
            predictions == 0,
            predictions == 1,
            predictions == 2,
            predictions == 3,
            predictions == 4,
            predictions == 5,
            predictions == 6,
            predictions == 7,

        ],
        [
            'facebook',
            'flickr',
            'google+',
            'instagram',
            'original',
            'telegram',
            'twitter',
            'whatsapp'
        ],
        predictions
    )


# get accuracy at patch level
def patch_truth(labels, predictions, classes):

    patch_truth = [label.decode('UTF-8').split('.')[0] for label in labels]

    print(classification_report(patch_truth, predictions, target_names=classes))


# get accuracy at image level
def image_truth(labels, predictions, classes):
    # decode
    y_test_im = []
    for y in labels:
        y_test_im.append(y.decode('UTF-8'))

    df = pd.DataFrame([y_test_im, predictions],
                      index=['truth', 'prediction']).T

    # group by class and image number
    grouped_df = df.groupby('truth', as_index=False)[
        'prediction'].agg(pd.Series.mode)
    # print(grouped_df.to_string())

    # split into respective image number
    grouped_df['truth'] = grouped_df['truth'].str.split('.').str[0]
    
    # get rid of non string values
    grouped_df = grouped_df[grouped_df['prediction'].apply(lambda x: isinstance(x, str))]

    image_truth = grouped_df['truth'].tolist()
    image_predictions = grouped_df['prediction'].tolist()

   
    print(classification_report(image_truth, image_predictions, target_names=classes))


def main(name, dataset_name, results):
    # user defined variables

    model = models.load_model(f'models/cnn_{name}')

    classes = ['facebook', 'flickr', 'google+', 'instagram',
               'original', 'telegram', 'twitter', 'whatsapp']

    # get the number of examples for the generator and steps
    num_examples = get_dset_len(f'{path[0]}/processed/DCT_test_{dataset_name}.h5', 'DCT')

    # predictions represented as integer representation of classes
    predictions = get_predictions(dataset_name, model, num_examples)

    # labels with string name and image indexes
    labels = get_labels(dataset_name)

    patch_truth(labels, predictions, classes)

    image_truth(labels, predictions, classes)


if __name__ == "__main__":
    main()
