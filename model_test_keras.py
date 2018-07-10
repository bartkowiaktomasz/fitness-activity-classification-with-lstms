import numpy as np
import pandas as pd
import keras
import seaborn as sns
import matplotlib.pyplot as plt

from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional
from keras.models import load_model, model_from_json
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split

from preprocessing import get_convoluted_data
from config import *

def one_hot_to_label(array):
    i = np.argmax(array)
    return LABELS_NAMES[i]

def softmax_to_one_hot(array):
    i = np.argmax(array)
    one_hot = np.zeros(len(array))
    one_hot[i] = 1
    return one_hot

model = load_model(MODEL_PATH)
data = pd.read_pickle(DATA_PATH)
data_convoluted, labels = get_convoluted_data(data)
_, X_test, _, y_test = train_test_split(data_convoluted, labels, test_size=TEST_SIZE, random_state=RANDOM_SEED, shuffle=True)

y_predicted = model.predict(X_test)
y_predicted = np.asarray([softmax_to_one_hot(y) for y in y_predicted])
for actual, predicted in zip(y_test, y_predicted):
    print("Actual: ", one_hot_to_label(actual), "\t Predicted: ", one_hot_to_label(predicted))

print("Final accuracy: ", accuracy_score(y_test, y_predicted))

cm = confusion_matrix(np.argmax(y_test, axis=1), np.argmax(y_predicted, axis=1))
plt.figure(figsize=(16, 14))
sns.heatmap(cm/(np.sum(cm, axis=1, keepdims=1)), xticklabels=LABELS_NAMES, yticklabels=LABELS_NAMES, annot=True);
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.title("Confusion matrix")
plt.show()
