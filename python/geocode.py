# ./weather-app/python/geocode.py
import requests

from urllib.parse import quote

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
