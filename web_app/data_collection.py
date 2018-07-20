"""
Run with
FLASK_APP=data_collection.py flask run --host=0.0.0.0
Accessible at http://192.168.1.71:5000
"""
import sys
sys.path.append("..") # Append higher directory

from flask import Flask, request, render_template
from ble_gatt import web_collect_save_data

from config import *

import os
app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        result = request.form['activity']
        web_collect_save_data(result)
    return render_template('choose_activity.html', activities=LABELS_NAMES)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
