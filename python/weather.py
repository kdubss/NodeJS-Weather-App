#!/usr/bin/python
# ./weather-app/python/weather.py
'''
Module to parse the JSON weather data from forecast.io (darksky.net) and to
make data manipulaions by using Pandas.
'''
import requests
import time
import argparse as ag
import pandas as pd

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
    (https://api.darksky.net/forecast/[key]/[latitude],[longitude],[time]) from
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
    from the call to the forecast.io API request (object returned as a response,
    which has a json() key with associated data values).
    '''
    hourly_data = weather_json_dict['hourly']['data']
    return hourly_data

def getMinutelyWeatherData(weather_json_dict):
    '''
    Function to parse out the minutely weather data from the JSON object returned
    from the call to the forecast.io API request (object returned as a response,
    which has a json() key with associated data values)
    '''
    minutely_data = weather_json_dict['minutely']['data']
    return minutely_data

def getHourlyDataSeries(weather_json_dict, data_param, series_name):
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
    TT = getHourlyDataSeries(hourly_data, data_param, series_name)
    return TT

def getDailyWeatherData(weather_json_dict):
    '''
    Function to get the daily weather data from the JSON object returned
    from the API request (to Darksky.net).
    '''
    daily_data = weather_json_dict['daily']
    return daily_data

def getDailyMinMaxDataSeries(weather_json_dict):
    '''
    Function to parse out and prepare the Daily Min. & Max. weather data into a
    pandas.core.series.Series object with weather data as the values
    and formatted (i.e. human-readable) dates as the series indices.
    '''
    daily_data = getDailyWeatherData(weather_json_dict)
    time

def getDailyMinMaxTemperature(weather_json_dict):
    '''
    Function to get and parse the 'temperature' parameter from the formatted
    JSON dictionary(JSON object returne from the API request to forecast.io).
    '''
    daily_data = getDailyWeatherData(weather_json_dict)
    TT_min = getDailyWEather(daily_data, 'temperaureMin', series_name)
    TT_max = getDailyT
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

def config1x1PlotLayout():
    '''
    Convenience function to configure the plot layout of single 1x1 plot layouts.
    '''
    plt.rc('font', family = 'serif')
    spines2cut = ['top', 'right']
    fig = plt.figure()
    fig.set_figwidth(15)
    fig.set_figheight(12)
    ax = fig.add_subplot(111)
    for ax in fig.get_axes():
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        for each_spine in spines2cut:
            ax.spines[each_spine].set_visible(False)
        for ylabel in ax.get_yticklabels():
            ylabel.set_fontsize(16)
        for xlabel in ax.get_xticklabels():
            xlabel.set_fontsize(16)
            xlabel.set_rotation(20)

def plotHourlyTemperature(hourly_TT_data_series):
    '''
    Function to visualize hourly-temperature data.
    '''
    config1x1PlotLayout()
    plt.show()

    # save_fig_title = 'test'
    # save_fig_fmt = '.svg'
    # save_fig_path = 'figs/'

def plotDailyTemprature(daily_TT_data_series):
    '''
    Function to visualize daily-temperature data.
    '''
    pass
    config1x1PlotLayout()
    plt.show()

def saveWeatherData2Csv(save_2_path):
    '''
    Function to save the parsed weather data-series to a directory defined by
    'save_2_path'.
    '''
    pass

if __name__ == '__main__':

    parser = ag.ArgumentParser(
        description = 'Module to parse and visualize weather data from forecast.io'
    )
    parser.add_argument(
        '-a',
        action = 'store',
        type = str,
        help = 'Address to fetch weather data for'
    )
    parser.add_argument(
        '-p',
        action = 'store_true',
        default = False,
        help = 'Boolean flag to trigger weather or not to plot the \
        hourly temperature / apparent-temperature data'
    )
    parser.add_argument(
        '--forecast',
        action = 'store_true',
        default = False,
        help = 'Boolean trigger to print out the details concerning \'forecast\' \
        requests to the DarkSky API.'
    )
    parser.add_argument(
        '--time_machine',
        action = 'store_true',
        default = False,
        help = 'Boolean trigger to print out the details concerning \'time-machine\' \
        requests to DarkSky API.'
    )
    args = parser.parse_args()

    if args.a == 'Vancouver' and args.p:
        address = 'Kitsilano Vancouver'
        json_data = getJSONWeatherData(address)
        json_dict = json_data.json()

        TT = getDailyTemperature(json_dict)

        plotDailyTemprature(TT)

    if args.forecast:
        showForecastRequestDocs()
    elif args.time_machine:
        showTimeMachineRequestDocs()
