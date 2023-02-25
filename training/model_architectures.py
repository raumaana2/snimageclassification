from keras import layers, models


def dct_cnn_2017(input_shape):
    input = layers.Input(shape=input_shape)
    conv1 = layers.Conv1D(100, 3, activation='relu')(input)
    max_pool1 = layers.MaxPooling1D()(conv1)
    conv2 = layers.Conv1D(100, 3, activation='relu')(max_pool1)
    max_pool2 = layers.MaxPooling1D()(conv2)
    flat = layers.Flatten()(max_pool2)
    dense1 = layers.Dense(units=256, activation='relu')(flat)
    dense2 =  layers.Dense(units=256)(dense1)
    dropout = layers.Dropout(rate=0.5)(dense2)
    output = layers.Dense(units=8, activation='softmax')(dropout)
    model = models.Model(inputs=input, outputs=output) 

    model.summary()

    model.compile(
        loss='categorical_crossentropy',
        optimizer='AdaDelta',
        metrics=['accuracy']
    )

    return model

def dct_cnn_2019(input_shape):
    input = layers.Input(shape=input_shape)
    conv1 = layers.Conv1D(100, 3, activation='relu')(input)
    max_pool1 = layers.MaxPooling1D()(conv1)
    conv2 = layers.Conv1D(100, 3, activation='relu')(max_pool1)
    max_pool2 = layers.MaxPooling1D()(conv2)
    flat = layers.Flatten()(max_pool2)
    dense1 = layers.Dense(units=1000, activation='relu')(flat)
    dropout1 = layers.Dropout(rate=0.5)(dense1)
    dense2 =  layers.Dense(units=1000)(dropout1)
    dropout2 = layers.Dropout(rate=0.5)(dense2)
    output = layers.Dense(units=8, activation='softmax')(dropout2)
    model = models.Model(inputs=input, outputs=output) 

    model.summary()

    model.compile(
        loss='categorical_crossentropy',
        optimizer='AdaDelta',
        metrics=['accuracy']
    )

    return model

def noise_cnn(input_shape):
    input = layers.Input(shape=input_shape)
    conv1 = layers.Conv2D(16, (3,3), activation='relu')(input)
    max_pool1 = layers.MaxPooling2D()(conv1)
    conv2 = layers.Conv2D(32, (3,3), activation='relu')(max_pool1)
    max_pool2 = layers.MaxPooling2D()(conv2)
    conv3 = layers.Conv2D(16, (3,3), activation='relu')(max_pool2)
    flat = layers.Flatten()(conv3)
    dense1 = layers.Dense(256, activation='swish')(flat)
    dropout1 = layers.Dropout(rate=0.5)(dense1)
    dense2 = layers.Dense(256, activation='swish')(dropout1)
    dropout2 = layers.Dropout(rate=0.5)(dense2)
    dense3 = layers.Dense(256, activation='swish')(dropout2)
    dropout3 = layers.Dropout(rate=0.5)(dense3)
    dense4 = layers.Dense(256, activation='swish')(dropout3)
    output = layers.Desnse(units=8, activation='softmax')(dense4)

    model = models.Model(inputs=input, outputs=output)

    model.summary()

    model.compile(
        loss='categorical_crossentropy',
        optimizer='Nadam',
        metrics=['accuracy']
    )

    return model



