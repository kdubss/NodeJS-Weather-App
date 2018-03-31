#!/usr/bin/python
# ./weather-app/python/weather.py
'''
Module to parse the JSON weather data from forecast.io (darksky.net) and to
make data manipulaions by using Pandas.
'''
import requests
import time
import argparse as arg
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

from local_settings import env
from geocode import getLatLon

def getCelsiusFromFarenheit(temp_farenheit):
    '''
    Function to convert temperature from farenheit to celsius.
    '''
    temp_celsius = (5/9) * (temp_farenheit - 32)
    return temp_celsius

def getFarenheitFromCelsius(temp_celsius):
    '''
    Function to convert temperature from celsius to farenheit
    '''
    temp_farenheit = ((9/5) * temp_celsius) + 32
    return temp_farenheit

def getJSONWeatherData(inputAddress):
    '''
    Function to retrieve the weather data from using the darksky.net API
    '''
    lat, lon = getLatLon(inputAddress)
    url = 'https://api.darksky.net/forecast/%s/%s,%s' % (env['forecastApiKey'],
                                                         str(lat), str(lon))
    r = requests.get(url)
    return r

def convertUnixTime2PST(unix_timestamp):
    '''
    Function to convert unix time stamp to PST time (localy here, in Vancouver)
    '''
    pretty_time = time.strftime('%d %b %Y %H:%M:%S +0000',
                                time.localtime(unix_timestamp))
    return pretty_time

def formatHourlyWeatherDictFromJSON(json_weather_dict):
    '''
    Function to format the weather data dict (retreived from the JSON API call)
    to a dict where the keys are the datetimes (formatted by the
    'formatWeatherDictFromJSON' function)
    '''
    hourly_dict_length = range(len(json_weather_dict))
    fmttd_weather_dict = {}

    for each_hr in hourly_dict_length:
        fmttd_weather_dict[convertUnixTime2PST(json_weather_dict['hourly']['data']\
                                               [each_hr]['time'])] = \
                           json_weather_dict['hourly']['data'][each_hr]

    return fmttd_weather_dict

def getHourlyWeatherData(weather_json_dict):
    '''
    Function to parse out the hourly weather data from the JSON object returned
    from the call to the forecast.io API request (object returned as an object).
    '''
    hourly_data = weather_json_dict['hourly']['data']
    return hourly_data

def getDataSeries(weather_json_dict, data_param, series_name):
    '''
    Function to parse out and prepare the weather data into a
    pandas.core.series.Series object with weather data as the values
    and formatted (i.e. human-readable) dates as the series indices.
    '''
    timestamp_series_list, data_series_list = [], []
    for each_data in weather_json_dict:
        timestamp_series_list.append(convertUnixTime2PST(each_data['time']))
        data_series_list.append(each_data[data_param])
    data_series = pd.Series(data_series_list, index = timestamp_series_list,
                            name = series_name)
    return data_series

def getHourlyTemperature(weather_json_dict):
    '''
    Function to get and parse the 'temperature' parameter from the
    formatted JSON dictionary (JSON object returned from the API request to
    forecast.io).
    '''
    hourly_data = getHourlyWeatherData(weather_json_dict)
    data_param = 'temperature'
    series_name = 'Hourly temperature data'
    TT = getDataSeries(hourly_data, data_param, series_name)
    return TT

def getHourlyApparentTemperature(weather_json_dict):
    '''
    Function to get and parse the 'apparentTemperature' parameter from the
    formatted JSON dictionary (JSON object returned from the API request to
    forecast.io).
    '''
    hourly_data = getHourlyWeatherData(weather_json_dict)
    data_param = 'apparentTemperature'
    series_name = 'Hourly apparent temperature'
    aTT = getDataSeries(hourly_data, data_param, series_name)
    return aTT

if __name__ == '__main__':

    address = 'Kitsilano Vancouver'
    json_data = getJSONWeatherData(address)
    json_dict = json_data.json()

    print('\nKeys in \'json_data\' dict object:\n')
    for ind, each_key in enumerate(json_dict.keys()):
        print(ind + 1, '\t', each_key)
    print('\n')

    print(getHourlyTemperature(json_dict), '\n')
    print(getHourlyApparentTemperature(json_dict))
