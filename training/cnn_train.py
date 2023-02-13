'''
Usage: python cnn_train.py {name} {EPOCH} {BATCH}
'''

from sys import argv, path 
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # get rid of the tf startup messages
from tensorflow.keras import models, callbacks
from sklearn import utils
import numpy as np
import h5py
import model_architectures
from matplotlib import pyplot as plt
from data_generator import data_generator

# obtain dataset lengths
# def get_dset_len(path, dset):
#     with h5py.File(path, 'r') as f:
#         return f[dset].shape[0]

def load_dset(path, dset):
    with h5py.File(path, 'r') as f:
        return f[dset], f[dset].shape[0]


def main(name, dataset_name, epoch, batch_size, architecture, his_range, sf_range):

    
    _, train_len = load_dset(f'{path[0]}/processed/DCT_train_{dataset_name}.h5', 'DCT')
    _, val_len = load_dset(f'{path[0]}/processed/DCT_val_{dataset_name}.h5', 'DCT')

    

    train_gen = data_generator(
        f'{path[0]}/processed/DCT_train_{dataset_name}.h5',
        f'{path[0]}/processed/labels_train_{dataset_name}.h5',
        train_len,
        batch_size,
    )
    val_gen = data_generator(
        f'{path[0]}/processed/DCT_val_{dataset_name}.h5',
        f'{path[0]}/processed/labels_val_{dataset_name}.h5',
        val_len,
        batch_size,
        False
    )



    # layers
    model = models.Sequential()

    input_shape = ((his_range[1]*2 + 1) * sf_range, 1)

    getattr(model_architectures, architecture)(model, input_shape)


    # early stopping to prevent doing unnecessary epochs
    # callback = callbacks.EarlyStopping(monitor='val_loss')

    # train
    history = model.fit(
        train_gen,
        # callbacks=[callback],
        epochs = epoch,
        validation_data=val_gen,
        use_multiprocessing=True,
        workers=16
    )
    
    model.save(f'models/cnn_{name}')

    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()

if __name__ == "__main__":
    main()