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
from config import *

# Hyperparameters-optimized (Bayesian optimization appends to that list)
hyperparametersOptimized = {'segment_time_size': [],
                            'time_step': [],
                            'learning_rate': [],
                            'n_hidden_neurons': [],
                            'droput_rate': [],
                            'n_epochs': [],
                            'batch_size': [],
                            'accuracy': []}

def createBidirectionalLSTM(segment_time_size,
                            n_hidden_neurons,
                            learning_rate,
                            droput_rate,
                            n_epochs,
                            batch_size,
                            X_train, y_train):

    X_train, X_val, y_train, y_val = train_test_split(X_train,
                                                      y_train, test_size=TEST_SIZE,
                                                      random_state=RANDOM_SEED+1,
                                                      shuffle=True)

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

def evaluate(segment_time_size,
             time_step,
             learning_rate,
             n_hidden_neurons,
             droput_rate,
             n_epochs,
             batch_size):

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

    model = createBidirectionalLSTM(segment_time_size,
                                    n_hidden_neurons,
                                    learning_rate,
                                    droput_rate,
                                    n_epochs,
                                    batch_size,
                                    X_train, y_train)

    y_predicted = model.predict(X_test)
    y_predicted = np.asarray([softmax_to_one_hot(y) for y in y_predicted])
    accuracy = accuracy_score(y_test, y_predicted)

    hyperparametersOptimized['segment_time_size'].append(segment_time_size)
    hyperparametersOptimized['time_step'].append(time_step)
    hyperparametersOptimized['learning_rate'].append(learning_rate)
    hyperparametersOptimized['n_hidden_neurons'].append(n_hidden_neurons)
    hyperparametersOptimized['droput_rate'].append(droput_rate)
    hyperparametersOptimized['n_epochs'].append(n_epochs)
    hyperparametersOptimized['batch_size'].append(batch_size)
    hyperparametersOptimized['accuracy'].append(accuracy)

    return accuracy


if __name__ == '__main__':

    # Load data
    data = pd.read_pickle(DATA_PATH)

    gp_params = {"alpha": 1e-5}
    evaluateBO = BayesianOptimization(evaluate, {'segment_time_size': (20, 100),
                                                 'time_step': (5, 50),
                                                 'learning_rate': (0.0005, 0.005),
                                                 'n_hidden_neurons': (5, 30),
                                                 'droput_rate': (0.2, 0.8),
                                                 'n_epochs': (10, 50),
                                                 'batch_size': (10, 50)})

    evaluateBO.explore({'segment_time_size': (20, 100),
                        'time_step': (5, 50),
                        'learning_rate': (0.0005, 0.005),
                        'n_hidden_neurons': (5, 30),
                        'droput_rate': (0.2, 0.8),
                        'n_epochs': (10, 50),
                        'batch_size': (10, 50)})

    evaluateBO.maximize(n_iter=25, **gp_params)

    print('Final Results')
    print('Evaluation: %f' % evaluateBO.res['max']['max_val'])

    np.save('hyperparametersOptimized.npy', hyperparametersOptimized)
