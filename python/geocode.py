# ./weather-app/python/geocode.py
import requests
import os
import pandas as pd

from urllib.parse import quote
from local_settings import env

address = 'Kitsilano Vancouver'

def getLatLon(inputAddress):
    '''
    Function to fetch the latitude, longitude from the Google Maps API
    using tne stdin of 'inputAddress'
    '''
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    encodedInputAddress = quote(inputAddress)
    apiAddress = url + encodedInputAddress

    r = requests.get(apiAddress)
    lat = r.json()['results'][0]['geometry']['location']['lat']
    lon = r.json()['results'][0]['geometry']['location']['lng']

    return lat, lon

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
