import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split
from tensorflow.python.tools import inspect_checkpoint as chkp

# Local libraries
from config import * # Global variables
from preprocessing import get_convoluted_data
from model_train import createBidirLSTM

##################################################
### FUNCTIONS
##################################################
def softmax_to_label(array):
    i = np.argmax(array)
    return LABELS_NAMES[i]

def evaluate(X_test, y_test):
    # Load the parameters
    with tf.Session() as sess:
        saver = tf.train.import_meta_graph(MODEL_META_PATH)
        saver.restore(sess, tf.train.latest_checkpoint(MODEL_CHECKPOINT_PATH))

        # Get the graph saved
        graph = tf.get_default_graph()

        X = graph.get_tensor_by_name("X:0")
        y = graph.get_tensor_by_name("y:0")
        y_pred_softmax = graph.get_tensor_by_name('y_pred_softmax:0')

        predictions = sess.run(y_pred_softmax, feed_dict={X: X_test})
        for actual, predicted in zip(y_test, predictions):
            print("Actual: ", softmax_to_label(actual), "\t Predicted: ", softmax_to_label(predicted))

        correct_pred = tf.equal(tf.argmax(y_pred_softmax, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_pred, dtype=tf.float32))

        acc = sess.run(accuracy, feed_dict={X: X_test, y: y_test})

        return acc

def preprocess_evaluate(data):
    data_convoluted, labels = get_convoluted_data(data)
    _, X_test, _, y_test = train_test_split(data_convoluted, labels, test_size=TEST_SIZE, random_state=RANDOM_SEED)
    accuracy = evaluate(X_test, y_test)
    print("Test set size: ", len(y_test))
    print("Final accuracy: ", accuracy)

def preprocess_evaluate_one_sample(sample):
    X_test, y_test = get_convoluted_data(sample, isOneSample=True)
    accuracy = evaluate(X_test, y_test)

##################################################
### MAIN
##################################################
if __name__ == '__main__':
    # data = pd.read_pickle(DATA_PATH)
    # preprocess_and_evaluate(data)

    sample = pd.read_pickle('data_temp/sample_Sitting_47.pckl')
    preprocess_evaluate_one_sample(sample)
