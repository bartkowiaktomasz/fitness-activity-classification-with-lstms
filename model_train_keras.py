from __future__ import print_function
import numpy as np
import pandas as pd

from keras.preprocessing import sequence
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional
from keras.datasets import imdb
from sklearn.model_selection import train_test_split

from preprocessing import get_convoluted_data
from config import *

# Load data
data = pd.read_pickle(DATA_PATH)
data_convoluted, labels = get_convoluted_data(data)
X_train, X_test, y_train, y_test = train_test_split(data_convoluted,
                                                    labels, test_size=TEST_SIZE,
                                                    random_state=RANDOM_SEED,
                                                    shuffle=True)


# Build a model
model = Sequential()
model.add(Bidirectional(LSTM(N_HIDDEN_NEURONS,
                        return_sequences=True,
                        activation="tanh"), input_shape=(SEGMENT_TIME_SIZE, N_FEATURES)))
model.add(Bidirectional(LSTM(N_HIDDEN_NEURONS)))
model.add(Dropout(0.5))
model.add(Dense(N_CLASSES, activation='sigmoid'))
model.compile('adam', 'binary_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train,
          batch_size=BATCH_SIZE,
          epochs=N_EPOCHS,
          validation_data=[X_test, y_test])

# Save the model
model.save(MODEL_PATH)
