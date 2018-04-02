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
import matplotlib.pyplot as plt
import matplotlib as mpl

from local_settings import env
from geocode import getLatLon

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

def getJSONWeatherData(inputAddress):
    '''
    Function to retrieve the weather data from using the darksky.net API
    '''
    lat, lon = getLatLon(inputAddress)
    url = 'https://api.darksky.net/forecast/%s/%s,%s' % (env['forecastApiKey'],
                                                         str(lat), str(lon))
    r = requests.get(url)
    return r

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

def getDailyWeatherData(weather_json_dict):
    '''
    Function to get the daily weather data from the JSON object returned
    from the API request (to Darksky.net).
    '''
    daily_data = weather_json_dict['daily']
    return daily_data

def getDataSeries(weather_json_dict, data_param, series_name):
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
    TT = getDataSeries(hourly_data, data_param, series_name)
    return TT

def getDailyTemperature(weather_json_dict):
    '''
    Function to get and parse the 'temperature' parameter from the formatted
    JSON dictionary(JSON object returne from the API request to forecast.io).
    '''
    daily_data = getDailyWeatherData(weather_json_dict)
    data_param = 'temperature'
    series_name = 'Daily temperature data'
    TT = getDataSeries(daily_data, data_param, series_name)
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
    Function to visualize hourly-temperature and hourly-apparent-temeperature
    data.
    '''
    config1x1PlotLayout()
    plt.show()

    # save_fig_title = 'test'
    # save_fig_fmt = '.svg'
    # save_fig_path = 'figs/'

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
    args = parser.parse_args()

    if args.a == 'Vancouver' and args.p:
        address = 'Kitsilano Vancouver'
        json_data = getJSONWeatherData(address)
        json_dict = json_data.json()

        TT = getHourlyTemperature(json_dict)
        TT_apparent = getHourlyApparentTemperature(json_dict)

        plotHourlyTemperature(TT)
