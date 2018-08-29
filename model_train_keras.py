"""
Script used to train the classifier.
It loads the data stored in the "DATA_PATH" path
(as specified in config file), and saves the trained
model at "MODEL_PATH".
"""

from __future__ import print_function
import numpy as np
import pandas as pd

from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Bidirectional
from keras.optimizers import Adam
from keras.datasets import imdb
from sklearn.model_selection import train_test_split

from preprocessing import get_convoluted_data
from config import *
from visualize import drawTrainTestHistory

def createBidirectionalLSTM(segment_time_size,
                            learning_rate,
                            n_hidden_neurons,
                            droput_rate,
                            n_epochs,
                            batch_size,
                            X_train, y_train,
                            X_val, y_val,
                            visualize=False):
    """
    Create a bidirectional Low-short term memory recurrent
    neural network for activity recognition.
    Input:
    - segment_time_size: size of a sliding window,
    - n_hidden_neurons: number of hidden neurons (nodes) in one layer,
    - learning_rate: learning rate used by the optimizer (Adam),
    - droput_rate: dropout rate during training,
    - n_epochs: number of epochs for training,
    - batch_size: batch size,
    - X_train, y_train, X_val, y_val: training and valuation data and labels.
    Returns sequential keras model.
    """
    # Build a model
    model = Sequential()
    model.add(Bidirectional(LSTM(n_hidden_neurons,
                            return_sequences=True,
                            activation="tanh"), input_shape=(segment_time_size, N_FEATURES),
                            merge_mode='sum'))
    model.add(Bidirectional(LSTM(n_hidden_neurons)))
    model.add(Dropout(droput_rate))
    model.add(Dense(N_CLASSES, activation='sigmoid'))
    adam_optimizer = Adam(lr=learning_rate, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    model.compile(optimizer=adam_optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    history = model.fit(X_train, y_train,
                        batch_size=batch_size,
                        epochs=n_epochs,
                        validation_data=[X_val, y_val])

    if(visualize):
        drawTrainTestHistory(history)

    return model


if __name__ == '__main__':

    # Load data
    data = pd.read_pickle(DATA_PATH)
    data_convoluted, labels = get_convoluted_data(data)
    X_train, X_val, y_train, y_val = train_test_split(data_convoluted,
                                                        labels, test_size=TEST_SIZE,
                                                        random_state=RANDOM_SEED,
                                                        shuffle=True)
    # Build a model
    model = createBidirectionalLSTM(SEGMENT_TIME_SIZE,
                                    LEARNING_RATE,
                                    N_HIDDEN_NEURONS,
                                    DROPOUT_RATE,
                                    N_EPOCHS,
                                    BATCH_SIZE,
                                    X_train, y_train,
                                    X_val, y_val,
                                    visualize=True)
    model.save(MODEL_PATH)
