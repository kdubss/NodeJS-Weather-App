#!/usr/bin/python
# ./weather-app/python/weather.py
'''
Module to parse the JSON weather data from forecast.io (darksky.net) and to
make data manipulaions by using Pandas.
'''
import argparse as ag
import pandas as pd

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
