import numpy as np
import pandas as pd
import keras

from keras.models import load_model
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.utils import shuffle

from visualize import drawConfusionMatrix
from preprocessing import get_convoluted_data, one_hot_to_label, softmax_to_one_hot
from config import *

def load_test_model(path):

    # Load model
    model = load_model(path)
    data = pd.read_pickle(DATA_PATH)
    X_test, y_test = get_convoluted_data(data)
    X_test, y_test = shuffle(X_test, y_test, random_state=0)

    # Make predictions
    y_predicted = model.predict(X_test)
    y_predicted = np.asarray([softmax_to_one_hot(y) for y in y_predicted])
    for actual, predicted in zip(y_test, y_predicted):
        print("Actual: ", one_hot_to_label(actual), "\t Predicted: ", one_hot_to_label(predicted))

    return y_predicted, y_test

if __name__ == '__main__':

    y_predicted, y_test = load_test_model(MODEL_PATH)
    print("Final accuracy: ", accuracy_score(y_test, y_predicted))

    # Confusion matrix
    cm = confusion_matrix(np.argmax(y_test, axis=1), np.argmax(y_predicted, axis=1))
    drawConfusionMatrix(cm)
