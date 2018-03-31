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

if __name__ == '__main__':

    address = 'Kitsilano Vancouver'
    json_data = getJSONWeatherData(address)
    json_dict = json_data.json()

    print('\nKeys in \'json_data\' dict object:\n')
    for ind, each_key in enumerate(json_dict.keys()):
        print(ind + 1, '\t', each_key)
    print('\n')
