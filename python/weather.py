# ./weather-app/python/weather.py
'''
Module to parse the JSON weather data from forecast.io (darksky.net) and to
make data manipulaions by using Pandas.
'''
import requests
import pandas as pd

from local_settings import env
from geocode import getLatLon

def getJSONWeatherData(inputAddress):
    '''
    Function to retrieve the weather data from using the darksky.net API
    '''
    lat, lon = getLatLon(inputAddress)
    url = 'https://api.darksky.net/forecast/%s/%s,%s' % (env['forecastApiKey'],
                                                         str(lat), str(lon))
    r = requests.get(url)
    return r

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
