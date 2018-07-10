# Run with
# FLASK_APP=web_app_data_collection.py flask run --host=0.0.0.0
# Accessible at http://192.168.1.71:5000

from flask import Flask, request, render_template
from ble_gatt import runWebBLE

from config import *

import os
app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        result = request.form['activity']
        runWebBLE(result)
    return render_template('index.html', activities=LABELS_NAMES)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
