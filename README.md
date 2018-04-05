# Weather-App: Node.js, Python/Pandas, D3.js, (React.js)

## Description

  *A CLI weather-tool / (app) which fetches a lat/lon coordinates of user-input address (postal codes, zip codes, cities, etc.), from the Google maps API, and uses those coordinates to fetch the past, current, and forecasted weather data from the forecast.io (darksky.net) API (requires an API-key).  Currently, this only functions as a CLI (command-line-interface) tool, where functionality is run by `Node.js` (e.g. `$node app.js -a [address]`) based on the user-input address*.

  *The* ***goal*** *of this project is to ultimately use `React.js` to create the font-end of an on-line app where* ***current***, ***hourly***, *and* ***minutely*** *weather data will be displayed, both visually as time-series figures and as data tables, depending on the input-address from the user.  Visual representation will be presented by using `D3.js`; Back-end will be powered by `Node.js` (currently, to __<u>test out and learn the `D3.js` library</u>__, the __back-end server will be powered by `Python`__); Data fetching, parsing, and manipulations will be done so using `Python/Pandas`*.

## API requests

### 1. *Forecast* requests
  - URL: `https://api.darksky.net/forecast/[key]/[latitude],[longitude]`
  - *returns the current weather conditions, a __minute-by-minute__ forecast for the __next hour__ (where available), an __hour-by-hour__ forecast for the next 48 hours, and a __day-by-day__ forecast for the next week*.

### 2. *Time-Machine* requests
  - URL: `https://api.darksky.net/forecast/[api-key]/[latitude],[longitude],[time]`
  - *Request returns the observed or forecast weather conditions for a date in the past or future (FOR THE SAKE OF THIS MVP --> FOCUS ON DATES IN THE PAST)*.

## Flask server

  - To run the Flask server, `cd` into `python/flask-d3/` from the projects' root directory.
  - Once there, run `python flask_server.py` to start the server (on `localhost::8080`)
  - __*End-points*__,
    - `/`: Index/home page (rendering `templates/index.html`)
      - The `/` end-point currently renders an `<ul>` element, listing `href` links for different parts of the project
        - For example, a listing of temperature parameters links directly to the D3 chart of that weather parameter (<i>i.e.</i> clicking on `Temperature` will take you to a static `html` page for the D3)
    - `/about`: Gives a summary of what the project is all about (<i>i.e.</i> what tech stack is used, what API is being used, etc.)

## D3.js charts

  - *Work-in-progress*
  - The __goal__ is to generate a figure like the one *below*, but using `D3.js` instead of [matplotlib](matplotlib.org).

![Line Chart](https://github.com/kdubss/NodeJS-Weather-App/blob/master/python/figs/test.png)

  - The figure above displays the hourly temperature data for both __*forecast*__ and __*time-machine*__ requests to the *Dark Sky API*.
  - For the two data-series' plotted above, there is an obvious region of overlap between the *hindcast* and *forecast* hourly temperature data returned, from the two API requests.
  - The *time machine* request above, was made for April 3, 2018, which means hourly temperatures from 03 Apr 00:00 to 03 Apr 23:00 are returned.
  - The *forecast* request was made @ ~ 14:00 today (April 3), which means there will be an overlap of > 7 hours.
    - This can be countered by either __a.__ cutting a slice of the data from the forecast data series, or __b.__ cutting a slice of the time-machine data series...  (*more to come*)

![D3 Render](https://github.com/kdubss/NodeJS-Weather-App/blob/master/imgs/forecast-temperature-d3.png)

  - The figure above is a rendered D3 line chart of the temperature data fetched from a forecast request for the time of April 4, 2018 at 11:00 am to April 7, 2018 at 11:00 am.
  - The __next step__ is to serve up this page from a Flask server end-point!

### Data Parameters (found at *[forecast.io](https://darksky.net)*) - Hourly Data
(for full details on request response formats, see [here](https://darksky.net/dev/docs#response-format))

  - `apparentTemperature`: 'feels like' temp in Farenheit
  - `cloudCover`: percentage of sky occluded by clouds, between 0 and 1, inclusive.
  - `dewPoint`: dew point in deg. Farenheit
  - `humidity`: relative humidity, between 0 and 1, inclusive
  - `icon`: machine-readable *text* summary of data-point, *suitable for selecting an **icon** for display*.
    - *If defined*
      - will have one of the following values,
        1. *`clear-day`*
        2. *`clear-night`*
        3. *`rain`*
        4. *`snow`*
        5. *`sleet`*
        6. *`wind`*
        7. *`fog`*
        8. *`cloudy`*
        9. *`partly-cloudy-day`*
        10. *`partly-cloudy-night`*
  - `ozone`: columnar density of total atmospheric ozone at the given time (in *Dobson units*)
  - `precipIntensity`: intensity (in *inches of liquid of water per hour*) of precipitation occurring at a given time.
  - `precipProbability`: probability of precipitation occurring, between 0 and 1, inclusive
  - `precipType`: type of precipitation occurring at a given time.
  - `pressure`: sea-level pressure in *millibars*
  - `summary`: human-readable text summary of data point
  - `temperature`: air-temp in deg. Farenheit
  - `time` (`unix` timestamp): `UNIX` time at which data point begins.
  - `uvIndex`: UV index
  - `visibility`: average visibility in *miles*, capped at 10 miles
  - `windBearing`: direction that the wind is coming *from* in degrees, with *true north* at 0$^o$ and progressing *clockwise*
  - `windGust`: wind gust in *miles / hr*
  - `windSpeed`: wind speed in *miles / hr*
