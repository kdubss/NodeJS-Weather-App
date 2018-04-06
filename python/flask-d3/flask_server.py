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

@app.errorhandler(404)
def pageNotFound(err):
    '''
    Handles a 404 client-side error(s).
    '''
    return (
        '''
        Sorry, 404!
        This means it's completely YOUR fault (i.e. wrong url, etc.).

        Make sure to get'yo stuff together and do it right!
        '''
    )

@app.errorhandler(500)
def serverError(err):
    '''
    Handles a 500 server-side error(s).
    '''
    return (
        '''
        Okay okay, okay...

        This is our fault...we'll do our best to get our stuff right, so you
        can get'yo stuff right!
        '''
    )

@app.route('/')
def getIndexPage():
    '''
    Rendering './templates/index.html'.
    '''
    return render_template('index.html')

@app.route('/forecast')
def getForeacastTemperatureD3():
    '''
    Parsing data and rendering the forecasted temperature data, then passing
    the data to ./templates/forecast_temperature.html, in which the data will
    be rendered by D3.
    '''
    return render_template('forecast_temperature.html')

@app.route('/hindcast')
def getHistoricalHindcastTemperatureD3():
    '''
    Parsing data and rendering the historical hindcast temperature data, then passing
    the data to ./templates/historical_temperature.html, in which the data will
    be rendered by D3.
    '''
    return render_template('historical_temperature.html')

@app.route('/temperature')
def getForecastAndHindcastTemperatureD3():
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
