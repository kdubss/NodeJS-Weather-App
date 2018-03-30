# ./weather-app/python/geocode.py
import requests
import pandas as pd

from urllib.parse import quote

googleMapsAPI = 'https://maps.googleapis.com/maps/api/geocode/json?address='
address = 'Kitsilano Vancouver'
encodedInputAddress = quote(address)
concatedUrl = googleMapsAPI + encodedInputAddress

r = requests.get(concatedUrl);

print(googleMapsAPI)
print(address)
print(encodedInputAddress)
print(concatedUrl)
print('\nStatus code of request: %i' % r.status_code)
