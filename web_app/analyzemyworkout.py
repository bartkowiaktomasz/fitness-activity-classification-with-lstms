"""
Analyze my workout web client.
Allows for activity classification. The script collects the data,
sends a JSON packet to the external server and displays the response
(prediction from the server).
Run with
FLASK_APP=analyzemyworkout.py python -m flask run --host=0.0.0.0
Accessible at http://192.168.1.71:5000
"""

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
        predicted_activity = web_collect_request()
        return render_template('activity_prediction.html', activity=predicted_activity, ip_local=IP_LOCAL)
    else:
        return render_template('index.html', ip_local=IP_LOCAL)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
