# Run with
# FLASK_APP=WebApp.py flask run --host=0.0.0.0
# Accessible at http://192.168.1.71:5000

from flask import Flask, request, render_template
from ble_gatt_web import runBLE
import os
app = Flask(__name__)

##################################################
### GLOBAL VARIABLES
##################################################
EXECUTABLE_SCRIPT = 'python ble_gatt_web.py'

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/rungatt', methods = ['POST', 'GET'])
def rungatt():
    if request.method == 'POST':
        result = request.form['activity']
        runBLE(result)
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
