"""
@file
@brief Taken from `mnist_cnn.py <https://github.com/fchollet/keras/blob/master/examples/mnist_cnn.py>`_.

Trains a simple convolution network on the :epkg:`MNIST` dataset.

Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
"""


def keras_mnist_data():
    """
    Retrieves the :epkg:`MNIST` database for :epkg:`keras`.
    """
    from keras.datasets import mnist
    from keras.utils import np_utils
    from keras import backend as K

    # the data, shuffled and split between train and test sets
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    img_rows, img_cols = 28, 28    # should be cmputed from the data

    try:
        imgord = K.image_data_format()
    except Exception:  # pylint: disable=W0703
        # older version
        try:
            imgord = K.common.image_dim_ordering()  # pylint: disable=E1101
        except Exception:  # pylint: disable=W0703
            # older version
            imgord = K.image_dim_ordering()  # pylint: disable=E1101

    if imgord == 'th':
        X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
        X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
    else:
        X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
        X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)

    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255

    # convert class vectors to binary class matrices
    nb_classes = len(set(y_train))
    Y_train = np_utils.to_categorical(y_train, nb_classes)
    Y_test = np_utils.to_categorical(y_test, nb_classes)
    return (X_train, Y_train), (X_test, Y_test)


def keras_build_mnist_model(nb_classes, fLOG=None):
    """
    Builds a :epkg:`CNN` for :epkg:`MNIST` with :epkg:`keras`.

    @param      nb_classes      number of classes
    @param      fLOG            logging function
    @return                     the model
    """
    from keras.models import Sequential
    from keras.layers import (
        Dense, Dropout, Activation, Flatten,
        Convolution2D, MaxPooling2D)
    from keras import backend as K

    try:
        imgord = K.image_data_format()
    except Exception:  # pylint: disable=W0703
        # older version
        try:
            imgord = K.common.image_dim_ordering()  # pylint: disable=E1101
        except Exception:  # pylint: disable=W0703
            # older version
            imgord = K.image_dim_ordering()  # pylint: disable=E1101

    model = Sequential()

    nb_filters = 32
    pool_size = (2, 2)
    kernel_size = (3, 3)
    img_rows, img_cols = 28, 28  # should be cmputed from the data

    fLOG("[keras_build_mnist_model] K.image_dim_ordering()={0}".format(imgord))
    if imgord == 'th':
        input_shape = (1, img_rows, img_cols)
    else:
        input_shape = (img_rows, img_cols, 1)

    try:
        model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                                padding='valid', input_shape=input_shape))
    except Exception:  # pylint: disable=W0703
        # older version
        model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                                border_mode='valid', input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])
    return model


def keras_fit(model, X_train, Y_train, X_test, Y_test, batch_size=128,
              nb_classes=None, epochs=12, fLOG=None):
    """
    Fits a :epkg:`keras` model.

    @param      model       :epkg:`keras` model
    @param      X_train     training features
    @param      Y_train     training target
    @param      X_test      test features
    @param      Y_test      test target
    @param      batch_size  batch size
    @param      nb_classes  nb_classes
    @param      epochs      number of iterations
    @param      fLOG        logging function
    @return                 model
    """
    # numpy.random.seed(1337)  # for reproducibility

    if nb_classes is None:
        nb_classes = Y_train.shape[1]
        if fLOG:
            fLOG("[keras_fit] nb_classes=%d" % nb_classes)
    try:
        model.fit(X_train, Y_train, batch_size=batch_size, epochs=epochs,
                  verbose=1, validation_data=(X_test, Y_test))
    except Exception:  # pylint: disable=W0703
        model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=epochs,
                  verbose=1, validation_data=(X_test, Y_test))
    return model


def keras_predict(model, X_test, Y_test):
    """
    Computes the predictions with a :epkg:`keras` model.

    @param      model       :epkg:`keras` model
    @param      X_test      test features
    @param      Y_test      test target
    @return                 score
    """
    score = model.evaluate(X_test, Y_test, verbose=0)
    return score
