# !/usr/bin/python
# ./weather-app/python/flask-d3/app.py

import json
import pandas as pd
import sys, os
import datetime as dt

from flask import Flask, render_template

sys.path.insert(0, '../')
import api_requests as api

from local_settings import env

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

@app.route('/test')
def getTestPage():
    '''
    Route for testing purposes.
    '''
    import api_requests as api
    import weather as w

    # > Fetching & Organization of data from API:
    forecast_request = api.getForecastDataFromDarkSkyAPI('Vancouver')
    forecast_json = forecast_request.json()
    forecast_hourly_data = forecast_json['hourly']['data']
    forecast_series = w.getForecastHourlyTemperatureSeries(forecast_hourly_data)
    forecast_df = w.convertSeriesData2DataFrame(forecast_series)
    w.saveWeatherData2Csv(forecast_df, 'data', 'forecast-hourly-temp-test.csv')

    # > Loading the data & passing it to html template:
    fname = 'forecast-hourly-temp-test.csv'
    df = pd.read_csv(env['path2data'] + fname)
    forecast_data = df.to_dict(orient = 'records')
    forecaset_data = json.dumps(forecast_data, indent = 2)
    data = { 'forecast_data' : forecast_data }
    return render_template('forecast_temperature.html', data = data)

@app.route('/')
def getIndexPage():
    '''
    Rendering './templates/index.html'.
    '''
    return render_template('index.html')

@app.route('/about')
def getAboutPage():
    '''
    Renderin './templates/about.html'
    '''
    return render_template('about.html')

@app.route('/forecast')
def getForeacastTemperatureD3():
    '''
    Parsing data and rendering the forecasted temperature data, then passing
    the data to ./templates/forecast_temperature.html, in which the data will
    be rendered by D3.
    '''
    import api_requests as api
    import weather as w

    # > Fetching & Organization of data from API:
    forecast_request = api.getForecastDataFromDarkSkyAPI('Vancouver')
    forecast_json = forecast_request.json()
    forecast_hourly_data = forecast_json['hourly']['data']
    forecast_series = w.getForecastHourlyTemperatureSeries(forecast_hourly_data)
    forecast_df = w.convertSeriesData2DataFrame(forecast_series)
    w.saveWeatherData2Csv(forecast_df, 'data', 'forecast-hourly-temp.csv')

    # > Passing data 2 D3.html
    path2Data = '~/Documents/node-projects/weather-app/python/flask-d3/data/'
    fname = 'forecast-hourly-temp'
    fname_fmt = '.csv'
    df = pd.read_csv(path2Data + fname + fname_fmt)
    forecast_data = df.to_dict(orient = 'records')
    forecast_data = json.dumps(forecast_data, indent = 2)
    data = { 'forecast_data': forecast_data }
    return render_template('forecast_temperature.html', data = data)

@app.route('/hindcast')
def getHistoricalHindcastTemperatureD3():
    '''
    Parsing data and rendering the historical hindcast temperature data, then passing
    the data to ./templates/historical_temperature.html, in which the data will
    be rendered by D3.
    '''
    import api_requests as api
    import weather as w
    import datetime as dt

    hindcast_request = api.getTimeMachineDataFromDarkSkyAPI('Vancouver',
                                                            str(dt.datetime.today() - dt.timedelta(1)))
    hindcast_json = hindcast_request.json()
    hindcast_hourly_data = hindcast_json['hourly']['data']
    hindcast_series = w.getTimeMachineHourlyTemperatureSeries(hindcast_hourly_data)
    hindcast_df = w.convertSeriesData2DataFrame(hindcast_series)
    w.saveWeatherData2Csv(hindcast_df, 'data', 'hindcast-hourly-temp.csv')

    path2Data = '~/Documents/node-projects/weather-app/python/flask-d3/data/'
    fname = 'hindcast-hourly-temp'
    fname_fmt = '.csv'
    df = pd.read_csv(path2Data + fname + fname_fmt)
    hindcast_data = df.to_dict(orient = 'records')
    hindcast_data = json.dumps(hindcast_data, indent = 2)
    data = { 'hindcast_data': hindcast_data }
    return render_template('historical_temperature.html', data = data)

@app.route('/temperature')
def getForecastAndHindcastTemperatureD3():
    '''
    Function to call when fetching the index endpoint.
    '''
    # path2Data = '~/Documents/node-projects/weather-app/python/flask-d3/data/'
    # fname = 'data.csv'
    # df = pd.read_csv(path2data + fname, sep = ',')
    # temp_data = df.to_dict(orient = 'records')
    # temp_data = json.dumps(temp_data, indent = 2)
    # data = { 'temp_data': temp_data }
    return render_template('test.html') # data = data)

if __name__ == '__main__':

    app.run(port = 8080, debug = True)
