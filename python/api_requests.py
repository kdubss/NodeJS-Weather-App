#./weather-app/python/api_requests.py
'''
Functions for url-requests to various API's (presently, forecast.io / DarkSky)
'''
import requests
import time

from dateutil import parser
from time import mktime

from local_settings import env
from geocode import getLatLon

def showForecastRequestDocs():
    '''
    Function to print out the forecast request (to the DarkSky API).
    '''
    print('\n',
        '''
        When making a request to the 'forecast' URL from DarkSky:
        (API responses consist of a UTF-8-encoded, JSON-formatted object)

        -----

        The returned object (request.models.Response type) has a \'.json()\'
        method, which returns a Python Dict object.

        Calling the .keys() - i.e. 'forecast.json().keys()' method on the dict
        will return the following Keys,

            1. 'flags'
            2. 'offset'
            3. 'hourly'
            4. 'timezone'
            5. longitude
            6. 'daily'
            7. 'latitude'
            8. 'currently'
            9. 'minutely'

        > 'flags':
            - Returns a Python Dict object
            - A flags object containing miscellaneous metadata about the request.
            - Keys,
                - 'sources':
                - 'isd-stations'
                - 'units'

        > 'offset':
            - deprecated (use timezone, instead)

        > 'currently'
        - SINGLE data point containing the current weather conditions
            at the requested location

        > 'minutely'
            - Data block containing weather conditions minute-by-minute for the
            next hour

        > 'hourly'
            - Data block containing the weather conditions day-by-day for the
            next two-days.

        > 'daily'
            - Data block containing the weather conditions day-by-day for the
            next week

        > 'latitude'
            - Requested latitude

        > 'longitude'
            - Requested longitude

        -----

        Some of the values returned for each key will be a 'data block object',

        > Data Block Objects:
            - Represents the various weather phenomena occurring over a period
            of time.
            - These objects contains the following properties:
                - 'data',
                    - Array of data points
                    - Ordered by time
                    - Describes the weather conditions at the requested location
                    (lat,lon) over time
                - 'summary':
                    - Human-readable summary of data block
            - *** CURRENTLY, FOR MVPs' SAKE --> ONLY CONCERNED WITH 'TEMPERATURE' ***
        ''', '\n'
    )

def showTimeMachineRequestDocs():
    '''
    Function to print out the forecast request (to the DarkSky API).
    '''
    print('\n'
        '''
        When making a request to the 'forecast' URL from DarkSky:
        (API responses consist of a UTF-8-encoded, JSON-formatted object)

        -----

        This request returns the observed or forecast weather conditions for a
        date in the past or future.
        (*** FOR THE SAKE OF THIS MVP --> FOCUS ON DATES IN THE PAST ***)

        URL: 'https://api.darksky.net/forecast/[key]/[latitude],[longitude],[time]'

        Time Machine Requests --> identical in structutre to Forecast requests
        EXCEPT,

            > 'currently'
                - Data point will refer to the TIME PROVIDED (...instead of current time)

            > 'minutely'
                - Data block will be ommitted...
                - Unless requesting a time WITHIN AN HOUR OF PRESENT

            > 'hourly'
                - Data block will contain data points STARTING AT MIDNIGHT (OF LOCAL TIME)
                of the DAY REQUESTED, and will continue until MIDNIGHT OF THE FOLLOWING
                DAY

                    - For example,
                        - A request is made for day = (t-2); where 't' = present day
                        - 'hourly' data block from the above request will start
                        from,

                            (00:00-local @ day = t-2) ==> (00:00-local @ day = t-1)

                    - See 'https://darksky.net/dev/docs#time-machine-request' for full
                    API-docs

            > 'daily'
                - Data block will only contain a SINGLE DATA POINT referring to the
                requested date.

            > 'alerts'
                - Data block omitted

        ''', '\n'
    )

def parseDateString2DateTimeObj(date):
    '''
    Function using the dateutil.parser.parse() function to parse any string date
    (e.g. '2018-04-03' or 'April 3, 2018') into a datetime object.

    INPUT:
        1. 'date'  ::  - Str object
                       - e.g. '2018-04-03' or 'April 3, 2018'
    OUTPUT:
        1. 'rdate'  ::  - Returned date object
    '''
    rdate = parser.parse(date)
    return rdate

def getForecastDataFromDarkSkyAPI(input_address):
    '''
    'Forecast' request to the forecast URL
    (https://api.darksky.net/forecast/[api-key]/[lat],[lon]) from the DarkSky
    API.

    INPUT:
        1. 'input_address'  ::  - Str input for the location of the API-request
                                - Can be a zip/postal code, actual street address,
                                or just a city name.
    OUTPUT:
        1. 'r'  ::  - r = the response output from the API request.
                    - The returned object (request.models.Response type) has a
                    '.json()' method, which returns a Python Dict object
                    (of key-value pair).
    '''
    lat, lon = getLatLon(input_address)
    url = 'https://api.darksky.net/forecast/%s/%s,%s' % (env['forecastApiKey'],
                                                         str(lat), str(lon))
    r = requests.get(url)
    return r

def getTimeMachineDataFromDarkSkyAPI(input_address, time):
    '''
    'Time-Machine' request to the time-machine-url
    (https://api.darksky.net/forecast/[api-key]/[latitude],[longitude],[time]) from
    the Dark Sky API.

    INPUT:
        1. 'input_address'  ::  - Str input for the location of the API-request
                                - Can be a zip/postal code, actual street address,
                                or just a city name.
        2. 'time'  ::  - UNIX timestamp
    OUTPUT:
        1. 'r'  ::  - r = the response output from the API request.
                    - The returned object (request.models.Response type) has a
                    '.json()' method, which returns a Python Dict object
                    (of key-value pair).
    '''
    unix_time = convertPSTTime2Unix(time)
    lat, lon = getLatLon(input_address)
    url = 'https://api.darksky.net/forecast/%s/%s,%s,%i' % (env['forecastApiKey'],
                                                            str(lat), str(lon),
                                                            int(unix_time))
    r = requests.get(url)
    return r

def convertPSTTime2Unix(readable_time):
    '''
    Functionality to convert Human readable time back to a UNIX time stamp
    Uses the datetime module and the 'mktime()' function, which uses the
    'struct_time' (full 9-tuple) which expresses the time in local time.
    Function returns a floating point number.

    INPUT:
        1. 'readable_time'  ::  - A human readable time
                                - E.g. '2018-04-02' or 'April 2, 2018'
    '''
    time = parser.parse(readable_time)
    unix_time = mktime(time.timetuple())
    return unix_time

def convertUnixTime2PST(unix_timestamp):
    '''
    Function to convert unix time stamp to PST time (localy here, in Vancouver)
    '''
    pretty_time = time.strftime('%d %b %H:%M',
                                time.localtime(unix_timestamp))
    return pretty_time
