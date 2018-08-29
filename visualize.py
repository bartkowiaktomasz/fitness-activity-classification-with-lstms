"""
Library used for data visualization.
If run alone, the script loads a keras model stored at "MODEL_PATH"
and saves its visualization to file.
Functions in this library do not return any value.
"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from drawnow import *
from config import *

def applyPlotStyle():
    """
    Internal function used by makePlot function to apply
    particular plot style (settings).
    """
    plt.grid(True)
    plt.xlim(0, plotRange_x)
    plt.ylim(-1 * plotRange_y, plotRange_y)
    plt.ylabel('Acceleration (da*g)')

def makePlot():
    """
    Function for plotting acceleration graphs
    (used by drawnow function).
    """
    plt.subplot(2,2,1)
    applyPlotStyle()
    plt.title('Acceleration x')
    plt.plot(ax, 'ro-', label='')

    plt.subplot(2,2,2)
    applyPlotStyle()
    plt.title('Acceleration y')
    plt.plot(ay, 'bo-', label='Acceleration y')

    plt.subplot(2,2,3)
    applyPlotStyle()
    plt.title('Acceleration z')
    plt.plot(az, 'go-', label='Acceleration z')

def drawConfusionMatrix(cm):
    """
    Take as input a confusion matrix
    (i.e. sklearn.metrics.confusion_matrix) and display it
    using a heatmap.
    """
    plt.figure(figsize=(14, 10))
    sns.set(font_scale=1.2)
    hm = sns.heatmap(cm/(np.sum(cm, axis=1, keepdims=1)), xticklabels=LABELS_NAMES, yticklabels=LABELS_NAMES, annot=True);
    hm.set_yticklabels(hm.get_yticklabels(), rotation=0)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.title("Confusion matrix")
    plt.show()

# Interface function for gatt tool
def drawGraphs(_ax, _ay, _az):
    """
    Interface function used by gatt data collection script.
    If boolean "visualize" is True in that script, this functin
    is revoked.
    """
    global ax
    global ay
    global az

    ax = _ax
    ay = _ay
    az = _az

    drawnow(makePlot)

def plot_keras_model(path):
    """
    Load a keras model and save its visualization to a file.
    """
    from keras.utils import plot_model
    from keras.models import load_model

    model = load_model(path)
    plot_model(model, to_file="model/model.png")

def drawTrainTestHistory(history):
    print(history.history.keys())

    # summarize history for accuracy
    plt.figure(figsize=(14, 10))
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

    # summarize history for loss
    plt.figure(figsize=(14, 10))
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

if __name__ == '__main__':
    plot_keras_model(MODEL_PATH)
