# ./weather-app/python/weather_plots.py
'''
Functions to visualize hourly weather data fetched from the Dark Sky API
'''
import matplotlib as mpl
import matplotlib.pyplot as plt

from weather import makeSave2Folder

def plotForecastedHourlyData(forecast_hourly, time_machine_hourly):
    '''
    Function to plot the hourly temperature data from the forecast request
    to the Dark Sky API.

    INPUT:
        1.  'forecast_hourly'  ::  - Pandas.core.series.Series object
                                   - Contains the temperature as the values and
                                   the datetimes (Day Month Hour:Min) as the
                                   Series indices
    '''
    fig = plt.figure(111)
    fig.set_figwidth(15)
    fig.set_figheight(14)
    axs = fig.add_subplot(111)

    spines2cut = ['top', 'right']
    for ax in fig.get_axes():
        for each_spine in spines2cut:
            ax.spines[each_spine].set_visible(False)
        for ylabel in ax.get_yticklabels():
            ylabel.set_fontsize(15)
        for xlabel in ax.get_xticklabels():
            xlabel.set_fontsize(15)
            xlabel.set_rotation(20)
        ax.plot(
            forecast_hourly, 'o-',
            lw = 4.5,
            alpha = 0.7,
            label = 'Forecast temperature'
        )
        ax.plot(
            time_machine_hourly, 'o-',
            lw = 4.5,
            alpha = 0.7,
            label = 'Time machine temperature'
        )
        ax.set_xlabel('\nDate Time (Month-Day hour)', fontsize = 18)
        ax.set_ylabel('Temperature $^{\circ}$F\n', fontsize = 18)
        ax.set_title('Forecast & Time-Machine Temperature Data\n\
                     (DarkSky API)\n', fontsize = 20)
        legend = ax.legend(
            loc = 'best',
            shadow = 'true',
            prop = {
                'size': 13,
            }
        )
        legend.get_frame().set_facecolor('khaki')
    fig.show()
    fig.savefig('figs/test.svg')

if __name__ == '__main__':

    from weather import *
    from api_requests import *

    forecast_req = getForecastDataFromDarkSkyAPI('Vancouver')
    forecast_data = forecast_req.json()['hourly']['data']
    forecast_series = getForecastHourlyTemperatureSeries(forecast_data)

    time_machine_req = getTimeMachineDataFromDarkSkyAPI('Vancouver', 'April 3, 2018')
    time_machine_data = time_machine_req.json()['hourly']['data']
    time_machine_series = getTimeMachineHourlyTemperatureSeries(time_machine_data)

    plotForecastedHourlyData(forecast_series, time_machine_series)
