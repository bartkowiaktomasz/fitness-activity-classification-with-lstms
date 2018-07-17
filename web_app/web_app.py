# Run with
# FLASK_APP=web_app.py python -m flask run --host=0.0.0.0
# Accessible at http://192.168.1.71:5000

from flask import Flask, request, render_template
from keras.models import load_model
from keras import backend
import sys
import tensorflow as tf
sys.path.append("..") # Append higher directory
from ble_gatt import web_collect_classify_activity
from preprocessing import one_hot_to_label

from config import *

import os
app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        # To allow using same model on different threads
        with backend.get_session().graph.as_default() as g:
            model = load_model(MODEL_PATH)
            y_predicted = web_collect_classify_activity(model)

            predicted_activity = one_hot_to_label(y_predicted)
            return render_template('activity.html', activity=predicted_activity)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
