# ./weather-app/python/weather.py
import pandas as pd
import requests

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
    return r.json()

if __name__ == '__main__':

    address = 'Kitsilano Vancouver'
    print(getJSONWeatherData(address))
