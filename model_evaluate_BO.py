"""
Script used for hyperparameters' optimization using
Bayesian Optimization (https://github.com/fmfn/BayesianOptimization)
Hyperparameters and their corresponding model performace are saved
as a dictionary in a .npy file.
"""

from __future__ import print_function
import numpy as np
import pandas as pd

from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Bidirectional
from keras.optimizers import Adam
from keras.datasets import imdb
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from bayes_opt import BayesianOptimization

from preprocessing import get_convoluted_data, softmax_to_one_hot
from model_train_keras import createBidirectionalLSTM
from config import *

# Hyperparameters-optimized (Bayesian optimization appends to that list)
hyperparameters_optimized = {'segment_time_size': [],
                            'time_step': [],
                            'learning_rate': [],
                            'n_hidden_neurons': [],
                            'droput_rate': [],
                            'n_epochs': [],
                            'batch_size': [],
                            'accuracy': []}

def evaluate(segment_time_size,
             time_step,
             learning_rate,
             n_hidden_neurons,
             droput_rate,
             n_epochs,
             batch_size):
    """
    Function used by a Bayesian optimizer. It takes as input
    the hyperparameters that are to be optimized:
    - segment_time_size: size of a sliding window,
    - time_step: step (shift) of the sliding window
    - learning_rate: learning rate used by the optimizer (Adam),
    - n_hidden_neurons: number of hidden neurons (nodes) in one layer,
    - droput_rate: dropout rate during training,
    - n_epochs: number of epochs for training,
    - batch_size: batch size.
    Return the accuracy of the classifier (measured on the test dataset).
    """

    # Convert to int (Bayesian optimization might select float values)
    segment_time_size = int(segment_time_size)
    time_step = int(time_step)
    n_hidden_neurons = int(n_hidden_neurons)
    n_epochs = int(n_epochs)
    batch_size = int(batch_size)

    data_convoluted, labels = get_convoluted_data(data, segment_time_size, time_step)
    X_train, X_test, y_train, y_test = train_test_split(data_convoluted,
                                                        labels, test_size=TEST_SIZE,
                                                        random_state=RANDOM_SEED,
                                                        shuffle=True)

    X_train, X_val, y_train, y_val = train_test_split(X_train,
                                                      y_train, test_size=TEST_SIZE,
                                                      random_state=RANDOM_SEED+1,
                                                      shuffle=True)

    model = createBidirectionalLSTM(segment_time_size,
                                    learning_rate,
                                    n_hidden_neurons,
                                    droput_rate,
                                    n_epochs,
                                    batch_size,
                                    X_train, y_train,
                                    X_val, y_val)

    y_predicted = model.predict(X_test)
    y_predicted = np.asarray([softmax_to_one_hot(y) for y in y_predicted])
    accuracy = accuracy_score(y_test, y_predicted)

    hyperparameters_optimized['segment_time_size'].append(segment_time_size)
    hyperparameters_optimized['time_step'].append(time_step)
    hyperparameters_optimized['learning_rate'].append(learning_rate)
    hyperparameters_optimized['n_hidden_neurons'].append(n_hidden_neurons)
    hyperparameters_optimized['droput_rate'].append(droput_rate)
    hyperparameters_optimized['n_epochs'].append(n_epochs)
    hyperparameters_optimized['batch_size'].append(batch_size)
    hyperparameters_optimized['accuracy'].append(accuracy)

    return accuracy


if __name__ == '__main__':

    # Load data
    data = pd.read_pickle(DATA_PATH)

    gp_params = {"alpha": 1e-5}
    evaluateBO = BayesianOptimization(evaluate, {'segment_time_size': (20, 100),
                                                 'time_step': (5, 50),
                                                 'learning_rate': (0.0005, 0.005),
                                                 'n_hidden_neurons': (5, 50),
                                                 'droput_rate': (0.2, 0.8),
                                                 'n_epochs': (10, 50),
                                                 'batch_size': (10, 50)})

    evaluateBO.explore({'segment_time_size': (20, 100),
                        'time_step': (5, 50),
                        'learning_rate': (0.0005, 0.005),
                        'n_hidden_neurons': (5, 50),
                        'droput_rate': (0.2, 0.8),
                        'n_epochs': (10, 50),
                        'batch_size': (10, 50)})

    evaluateBO.maximize(n_iter=30, **gp_params)

    print('Final Results')
    print('Evaluation: %f' % evaluateBO.res['max']['max_val'])

    np.save('hyperparameters_optimized.npy', hyperparameters_optimized)
