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

def createBidirectionalLSTM(X_train, X_val, y_train, y_val):

    # Build a model
    model = Sequential()
    model.add(Bidirectional(LSTM(N_HIDDEN_NEURONS,
                            return_sequences=True,
                            activation="tanh"), input_shape=(SEGMENT_TIME_SIZE, N_FEATURES)))
    model.add(Bidirectional(LSTM(N_HIDDEN_NEURONS)))
    model.add(Dropout(DROPOUT_RATE))
    model.add(Dense(N_CLASSES, activation='sigmoid'))
    adam_optimizer = Adam(lr=LEARNING_RATE, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    model.compile(optimizer=adam_optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train,
              batch_size=BATCH_SIZE,
              epochs=N_EPOCHS,
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
    model = createBidirectionalLSTM(X_train, X_val, y_train, y_val)
    model.save(MODEL_PATH)
