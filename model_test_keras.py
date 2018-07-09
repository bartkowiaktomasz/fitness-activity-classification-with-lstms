import numpy as np
import pandas as pd
import keras

from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional
from keras.models import load_model, model_from_json
from sklearn.model_selection import train_test_split

from preprocessing import get_convoluted_data
from config import *

def softmax_to_label(array):
    i = np.argmax(array)
    return LABELS_NAMES[i]

model = load_model('model_keras/model.h5')
data = pd.read_pickle(DATA_PATH)
data_convoluted, labels = get_convoluted_data(data)
X_train, X_test, y_train, y_test = train_test_split(data_convoluted, labels, test_size=TEST_SIZE, random_state=RANDOM_SEED, shuffle=True)

classes = model.predict(X_test)
for actual, predicted in zip(y_test, classes):
    print("Actual: ", softmax_to_label(actual), "\t Predicted: ", softmax_to_label(predicted))
