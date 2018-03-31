# ./weather-app/python/weather.py
'''
Module to parse the JSON weather data from forecast.io (darksky.net) and to
make data manipulaions by using Pandas.
'''
import requests
import time
import pandas as pd

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
    pretty_time = time.strftime('%d %b %Y %H:%M:%S +0000', time.localtime(unix_timestamp))
    return pretty_time

def formatHourlyWeatherDictFromJSON(json_weather_dict):
    '''
    Function to format the weather data dict (retreived from the JSON API call)
    to a dict where the keys are the datetimes (formatted by the 'formatWeatherDictFromJSON'
    function)
    '''
    hourly_dict_length = range(len(json_weather_dict))
    fmttd_weather_dict = {}

    for each_hr in hourly_dict_length:
        fmttd_weather_dict[convertUnixTime2PST(json_weather_dict['hourly']['data'][each_hr]['time'])] = \
                           json_weather_dict['hourly']['data'][each_hr]

    return fmttd_weather_dict

if __name__ == '__main__':

    address = 'Kitsilano Vancouver'
    json_data = getJSONWeatherData(address)
    json_dict = json_data.json()

    print('\nKeys in \'json_data\' dict object:\n')
    for ind, each_key in enumerate(json_dict.keys()):
        print(ind + 1, '\t', each_key)
    print('\n')

    # print(json_dict['currently'])
    # print('\n', json_dict['hourly'])
    # print('\n', json_dict['hourly']['data'][0])
    print(len(json_dict['hourly']['data']))
