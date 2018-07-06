# Run with
# FLASK_APP=WebApp.py flask run --host=0.0.0.0
from flask import Flask, request, render_template
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
        os.system(EXECUTABLE_SCRIPT + ' ' + result)
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
