#!/usr/bin/python
# ./weather-app/python/weather.py
'''
Module to parse the JSON weather data from forecast.io (darksky.net) and to
make data manipulaions by using Pandas.
'''
import os
import argparse as ag
import datetime as dt
import pandas as pd

import api_requests as dsky

def getCelsiusFromFarenheit(temp_farenheit):
    '''
    Function to convert temperature from farenheit to celsius.

    INPUT:
        1. 'temp_farenheit'  ::  - temperature in farenheit
    OUTPUT:
        1. 'temp_celsius'  ::  - temperature in celsius
    '''
    temp_celsius = (5/9) * (temp_farenheit - 32)
    return temp_celsius

def getFarenheitFromCelsius(temp_celsius):
    '''
    Function to convert temperature from celsius to farenheit

    INPUT:
        1. 'temp_celsius'  ::  - temperture in celsius
    OUTPUT:
        1. 'temp_farenheit'  ::  - temperature in farenheit
    '''
    temp_farenheit = ((9/5) * temp_celsius) + 32
    return temp_farenheit

def getHourlyWeatherData(weather_json_dict):
    '''
    Function to parse out the hourly weather data from the JSON object returned
    from the call to the forecast.io API request (object returned as a response,
    which has a json() key with associated data values).
    '''
    hourly_data = weather_json_dict['hourly']['data']
    return hourly_data

def getForecastHourlyTemperatureSeries(hourly_weather_list):
    '''
    Function to parse out and prepare the weather data into a
    pandas.core.series.Series object with weather data as the values
    and formatted (i.e. human-readable) dates as the series indices.

    INPUT:
        1. 'hourly_weather_list'  ::  - List object of the hourly data from the
                                      response object returned from
                                      the forecast request to the DarkSky API.
                                      - For 'forecast' requests --> hourly data is returned
                                      for the next days (48 hrs).
                                      - Input is a list of dictionary objects, one for
                                      each hour in the next 2 days.
    OUTPUT:
        1. 'hourly_series'  ::  - Pandas.core.series.Series object of temperature
                                data fetched from the DarkSky API.
                                - Series constructed from 2 lists; 1 containing
                                the temperture values from the 'hourly_list' input,
                                the other containing human-readable datetimes,
                                also parsed from the 'hourly_weather_list' input.
    '''
    timestamp_series_list, data_series_list = [], []
    for each_hrs_data in hourly_weather_list:
        timestamp_series_list.append(dsky.convertUnixTime2PST(each_hrs_data['time']))
        data_series_list.append(each_hrs_data['temperature'])
    hourly_series = pd.Series(
        data_series_list,
        index = timestamp_series_list,
        name = 'Forecasted hourly temperature data series'
    )
    return hourly_series

def getTimeMachineHourlyTemperatureSeries(hourly_weather_list):
    '''
    Function to parse out and prepare the weather data into a
    pandas.core.series.Series object with weather data as the values
    and formatted (i.e. human-readable) dates as the series indices.

    INPUT:
        1. 'hourly_weather_list'  ::  - List of the hourly data returned from the
                                      response object returned from the timeMachine
                                      request to the DarkSky API.
                                      - Series constructed from 2 lists; 1 containing
                                      the temperture values from the 'hourly_list' input,
                                      the other containing human-readable datetimes,
                                      also parsed from the 'hourly_weather_list' input.
                                      - RECALL that the time-machine requests will only
                                      return 24-hrs worth of data (for hourly data)
                                      from midnight (day = t - 2) of the day specified
                                      on request, to midnight of the following day
                                      (day = t - 1).
    OUTPUT:
        1. 'hourly_series'  ::  - Pandas.core.series.Series object of temperature
                                data fetched from the DarkSky API.
                                - Series constructed from 2 lists; 1 containing
                                the temperture values from the 'hourly_weather_list' input,
                                the other containing human-readable datetimes,
                                also parsed from the 'hourly_weather_list' input.
    '''
    timestamp_series_list, data_series_list = [], []
    for each_hrs_data in hourly_weather_list:
        timestamp_series_list.append(dsky.convertUnixTime2PST(each_hrs_data['time']))
        data_series_list.append(each_hrs_data['temperature'])
    hourly_series = pd.Series(
        data_series_list,
        index = timestamp_series_list,
        name = 'Time-machine hourly temperature data series'
    )
    return hourly_series

def makeSave2Folder(directoy_or_path, dir_name):
    '''
    Function to create a directory (path) in which to save stuff (i.e. data, figs)
    to.
    If the directory with 'dir_name' already exists, then the save operation will
    be conducted on the same folder (i.e. 'dir_name').

    INPUT:
        1. 'directory_or_path'  ::  - Absolute or relative directory in which to
                                    create the folder in which to save stuff into
                                    - Str object
        2. 'dir_name'  ::  - Name of the folder to create.
                           - Str object
    '''
    if os.path.isdir(directoy_or_path + '/' + dir_name):
        print('\nThe folder already exists!\n')
    else:
        os.mkdir(directoy_or_path + '/' + dir_name)
        print('\nThe folder %s has been successfully created!\n' % dir_name)

def saveWeatherData2Csv(data_2_save, save_2_path, fname):
    '''
    Function to save the parsed weather data-series to a directory defined by
    'save_2_path'.

    INPUT:
        1. 'save_2_path'  ::  - Absolute or relative path of where to save the data.
        2. 'dir_name'  ::  - Name of the folder in which the save action is to be
                           performed
    OUTPUT:
        1. none  ::  - No output
                     - Function saves figure from data series' (.csv format) into
                     the path defined by 'save_2_path'.
    '''
    fname = fname
    data_2_save.to_csv(save_2_path + '/' + fname, index = True)

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
    parser.add_argument(
        '--time',
        action = 'store',
        type = str
    )

    args = parser.parse_args()

    if args.forecast and args.a:
        forecast_request = dsky.getForecastDataFromDarkSkyAPI(args.a)
        forecast_data = forecast_request.json()
        hourly = forecast_data['hourly']['data']
        hourly_series = getForecastHourlyTemperatureSeries(hourly)
        saveWeatherData2Csv(hourly_series, 'csv', 'forecast-hourly-temp.csv')
        print('\nFetching forecast weather data for %s\n(using the DarkSky API)\n' % args.a)
        print(hourly_series)

    elif args.time_machine and args.time and args.a:
        time_machine_request = dsky.getTimeMachineDataFromDarkSkyAPI(args.a, args.time)
        past_data = time_machine_request.json()
        past_hourly = past_data['hourly']['data']
        past_series = getTimeMachineHourlyTemperatureSeries(past_hourly)
        saveWeatherData2Csv(past_series, 'csv', 'past-hourly-temp.csv')
        print('\nFetching time-machine weather data for %s (from %s to %s midnight)\n' % \
              (args.a, dsky.parseDateString2DateTimeObj(args.time), dt.date.today()))
        print(past_series)
