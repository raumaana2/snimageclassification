from sys import path 
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # get rid of the tf startup messages
from tensorflow.keras import models, callbacks
import h5py
import model_architectures
from matplotlib import pyplot as plt
from data_generator import data_generator
import numpy as np



def get_dset_len(path):
    with h5py.File(path, 'r') as f:
        return f['DCT'].shape[0]



def main(name, epoch, batch_size, architecture, input):

    
    train_len = get_dset_len(f'{path[0]}/processed/DCT_train_{input.dset_name}.h5')
    val_len = get_dset_len(f'{path[0]}/processed/DCT_val_{input.dset_name}.h5')

    
    train_gen = data_generator(
        f'{path[0]}/processed/DCT_train_{input.dset_name}.h5',
        'DCT',
        train_len,
        batch_size,
    )
    val_gen = data_generator(
        f'{path[0]}/processed/DCT_val_{input.dset_name}.h5',
        'DCT',
        val_len,
        batch_size
    )



   

    input_shape = (input.his_size, 1)

    model = getattr(model_architectures, architecture)(input_shape)


    # early stopping to prevent doing unnecessary epochs
    # callback = callbacks.EarlyStopping(monitor='val_loss')

    # train
    history = model.fit(
        train_gen,
        # callbacks=[callback],
        # class_weight=class_weights_dict,
        epochs = epoch,
        validation_data=val_gen,
        use_multiprocessing=True,
        workers=8
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