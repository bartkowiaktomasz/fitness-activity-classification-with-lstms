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

def createBidirectionalLSTM(segment_time_size,
                            n_hidden_neurons,
                            learning_rate,
                            droput_rate,
                            n_epochs,
                            batch_size,
                            X_train, y_train,
                            X_val, y_val):

    # Build a model
    model = Sequential()
    model.add(Bidirectional(LSTM(n_hidden_neurons,
                            return_sequences=True,
                            activation="tanh"), input_shape=(segment_time_size, N_FEATURES)))
    model.add(Bidirectional(LSTM(n_hidden_neurons)))
    model.add(Dropout(droput_rate))
    model.add(Dense(N_CLASSES, activation='sigmoid'))
    adam_optimizer = Adam(lr=learning_rate, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    model.compile(optimizer=adam_optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train,
              batch_size=batch_size,
              epochs=n_epochs,
              validation_data=[X_val, y_val])

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
                                    N_HIDDEN_NEURONS,
                                    LEARNING_RATE,
                                    DROPOUT_RATE,
                                    N_EPOCHS,
                                    BATCH_SIZE,
                                    X_train, y_train,
                                    X_val, y_val)
    model.save(MODEL_PATH)
