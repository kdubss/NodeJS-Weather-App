# !/usr/bin/python
# ./weather-app/python/flask-d3/app.py

import json
import pandas as pd
import sys, os
import datetime as dt

from flask import Flask, render_template, url_for

sys.path.insert(0, '../')
import api_requests as api
import weather as w

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
@app.route('/index')
def getIndex():
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
def getForecastTemperatureD3():
    '''
    Parsing data and rendering the forecasted temperature data, then passing
    the data to ./templates/forecast_temperature.html, in which the data will
    be rendered by D3.
    '''
    # > Fetching and prepping forecast temperature data:
    forecast_request = api.getForecastDataFromDarkSkyAPI('Vancouver')
    forecast_hourly_data = forecast_request.json()['hourly']['data']
    forecast_hourly_series = w.getForecastHourlyTemperatureSeries(forecast_hourly_data)
    forecast_df = w.convertSeriesData2DataFrame(forecast_hourly_series)
    w.saveWeatherData2Csv(forecast_df, 'data', 'forecast-hourly-temp.csv')

    # > loading and sending forecast temperature data to html template:
    path2Data = '~/Documents/node-projects/weather-app/python/flask-d3/data/'
    fname = 'forecast-hourly-temp'
    fname_fmt = '.csv'
    df = pd.read_csv(path2Data + fname + fname_fmt)
    forecast_data = df.to_dict(orient = 'records')
    forecast_data = json.dumps(forecast_data, indent = 2)
    data = { 'forecast_data': forecast_data }

    return render_template(
        'forecast-temp.html',
        data = data,
        title = 'Forecasted Hourly Temp (from %s on)' % str(dt.datetime.today())
    )

@app.route('/hindcast')
def getHistoricalHindcastTemperatureD3():
    '''
    Parsing data and rendering the historical hindcast temperature data, then passing
    the data to ./templates/historical_temperature.html, in which the data will
    be rendered by D3.
    '''
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

    return render_template(
        'hindcast-temp.html',
        data = data,
        title = 'Historical Hourly Temp (from %s)' % str(dt.datetime.today() - dt.timedelta(1))
    )

@app.route('/temperature')
def getForecastAndHindcastTemperatureD3():
    '''
    Function to call when fetching the index endpoint.
    '''
    import datetime as dt

    import api_requests as api
    import weather as w

    # > Making requests to API:
    forecast_request = api.getForecastDataFromDarkSkyAPI('Vancouver')
    hindcast_request = api.getTimeMachineDataFromDarkSkyAPI('Vancouver', str(dt.datetime.today()))

    forecast_hourly_data = forecast_request.json()['hourly']['data']
    forecast_series = w.getForecastHourlyTemperatureSeries(forecast_hourly_data)
    hindcast_hourly_data = hindcast_request.json()['hourly']['data']
    hindcast_series = w.getTimeMachineHourlyTemperatureSeries(hindcast_hourly_data)

    df = w.combineForecastAndTimemachineSeries2DfAndSave(forecast_series, hindcast_series)
    df.to_csv('data/combined-temp-data.csv', index = False)

    # > Loading up and passing data to D3:
    path2Data = '~/Documents/node-projects/weather-app/python/flask-d3/data/'
    fname = 'combined-temp-data.csv'
    df = pd.read_csv(path2Data + fname, sep = ',')
    temp_data = df.to_dict(orient = 'records')
    temp_data = json.dumps(temp_data, indent = 2)
    data = { 'temp_data': temp_data }
    
    return render_template(
        'forecast-hindcast-temp.html',
        data = data
    )

@app.route('/inheritance')
def getInheritanceTest():
    return render_template('inheritance-test.html')

if __name__ == '__main__':

    app.run(port = 8080, debug = True)
