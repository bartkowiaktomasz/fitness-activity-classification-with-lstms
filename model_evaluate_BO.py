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

    return accuracy


if __name__ == '__main__':

    # Load data
    data = pd.read_pickle(DATA_PATH)
    acc = evaluate(SEGMENT_TIME_SIZE,
                   TIME_STEP,
                   LEARNING_RATE,
                   N_HIDDEN_NEURONS,
                   DROPOUT_RATE,
                   N_EPOCHS,
                   BATCH_SIZE)

    print("Accuracy: ", acc)

    """
    gp_params = {"alpha": 1e-5}
    evaluateBO = BayesianOptimization(evaluate, {'': (100, 1000),
                                                 'N_HIDDEN_NEURONS': (5, 30),
                                                 'BATCH_SIZE': (10, 100)})

    evaluateBO.explore({'SEGMENT_TIME_SIZE': [100, 1000],
                        'N_HIDDEN_NEURONS': [5, 30],
                        'BATCH_SIZE': [10, 100]})

    evaluateBO.maximize(n_iter=10, **gp_params)

    print('Final Results')
    print('Evaluation: %f' % evaluateBO.res['max']['max_val'])
    """
