# Run with
# FLASK_APP=main.py python -m flask run --host=0.0.0.0
# Accessible at http://192.168.1.71:5000

from flask import Flask, request, render_template
import sys

sys.path.append("..") # Append higher directory

from ble_gatt import web_collect_request
from preprocessing import one_hot_to_label

from config import *

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        response = web_collect_request()
        return render_template('activity.html', activity=response)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
