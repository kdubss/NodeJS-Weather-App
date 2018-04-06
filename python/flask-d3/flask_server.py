# !/usr/bin/python
# ./weather-app/python/flask-d3/app.py

import json
import pandas as pd
import sys, os
import datetime as dt

from flask import Flask, render_template

sys.path.insert(0, '../')
import api_requests as api

app = Flask(__name__)

@app.route('/')
def index():
    '''
    Function to call when fetching the index endpoint.
    '''
    # path2data = '~/Documents/node-projects/weather-app/python/flask-d3/data/'
    # fname = 'data.csv'
    # df = pd.read_csv(path2data + fname, sep = ',')
    # temp_data = df.to_dict(orient = 'records')
    # temp_data = json.dumps(temp_data, indent = 2)
    # data = { 'temp_data': temp_data }
    return render_template('test.html') # data = data)

if __name__ == '__main__':

    app.run(port = 8080, debug = True)
