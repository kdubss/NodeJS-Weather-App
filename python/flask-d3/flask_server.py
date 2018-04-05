# ./weather-app/python/flask_server.py
import os, sys
import datetime as dt

from flask import Flask, request, session, flash, render_template, redirect

sys.path.insert(0, '../')
import api_requests as dsky

from geocode import getLatLon

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.errorhandler(404)
def url_err(err):
    return '''
        Invalid URL end-point!
    '''

@app.errorhandler(500)
def server_err(err):
    return '''
        Internal server error!
    '''

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/forecast_temperature')
def show_temp_d3():
    return render_template('testing-dsky-d3.html')

if __name__ == '__main__':

    app.run(port = 8080, debug = True)
