# ./weather-app/python/geocode.py
import requests
import pandas as pd

from urllib.parse import quote

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

    

# > For Testing:
# print(googleMapsAPI)
# print(address)
# print(encodedInputAddress)
# print(concatedUrl)
# print('\nStatus code of request: %i' % r.status_code)
