kk# Weather-App: `JavaScript`, `Python/Pandas`, `D3.js`, (`React.js`)

## <a id='toc'>Table Of Contents</a>

[Still to do...](#todostill)

  1. [Description](#description)
  2. [CLI-Tool](#cli-tool)</a>
  3. [Web-App](#webapp)</a>
  4. [API-Requests](#api)</a>
  5. [Flask-Server](#flask-server)
  6. [D3.js](#d3)
  7. [Weather Data Parameters](#data)

## <a id='description'>Description</a>
  *A CLI weather-tool / (app) which fetches a lat/lon coordinates of user-input address (postal codes, zip codes, cities, etc.), from the Google maps API, and uses those coordinates to fetch the past, current, and forecasted weather data from the forecast.io (darksky.net) API (requires an API-key).  Currently, this only functions as a CLI (command-line-interface) tool, where functionality is run by `Node.js` (e.g. `$node app.js -a [address]`) based on the user-input address*.

  *The* ***goal*** *of this project is to ultimately use `React.js` to create the font-end of an on-line app where* ***current***, ***hourly***, *and* ***minutely*** *weather data will be displayed, both visually as time-series figures and as data tables, depending on the input-address from the user.  Visual representation will be presented by using `D3.js`; Back-end will be powered by `Node.js` (currently, to __<u>test out and learn the `D3.js` library</u>__, the __back-end server will be powered by `Python`__); Data fetching, parsing, and manipulations will be done so using `Python/Pandas`*.

[Back 2 ToC](#toc) &#128070;

### 1. <a id='cli-tool'>Command-Line-Tool</a> (written in `JavaScript`)
  *The CLI tool is a quick way of fetching the current weather conditions from the __DarkSky__ API.  Simply call the __`app.js`__ script via. __`node`__ and the __`-a`__ flag to specify a specific address (either a city's name - i.e. Vancouver, or a postal/zip code, or even a country's name) to output the __current weather conditions__ for the specified address.*

![fetch_by_name](https://github.com/kdubss/NodeJS-Weather-App/blob/master/imgs/fetch_by_name.png)
  - Fetching the current weather by a city's name.

![fetch_by_zip](https://github.com/kdubss/NodeJS-Weather-App/blob/master/imgs/fetch_by_zip.png)
  - Fetching the current weather by a city's zip-code

![fetch_by_country](https://github.com/kdubss/NodeJS-Weather-App/blob/master/imgs/fetch_by_country.png)
  - Fetching the current weather by a country's name

  [Back 2 ToC](#toc) &#128070;

### 2. <a id='webapp'>Web-App</a> (work-in-progress; written in `Python/D3.js`)
  *The __web-app__ is still a work-in-progress, but from the current code there is a currently functional __MVP__ with the current code-base.*
  *Currently, there are two parts to the MVP.  Firstly, `weather.py` is run, to fetch the weather data from the DarkSky API.  Second, when all the data has been fetched, parsed, and saved, the Flask server passes the data to the static html files that renders the data using `D3`.*

  #### <a id='todostill'>Still to do</a>:
  __1.__ Revise the `D3` code to be more modular &#x2192; __*complete*__
      - Also, research and fix the `D3` to render the temperature data returned from both the __forecast__ and __time-machine__ requests. &#x2192; __*complete*__ (*the problem was the x/y-axis min/max limits between the two data sets being used, I think...*)

  - The __`D3`__ rendered figure for the __`/hindcast`__ end-point is missing both the y-axis and x-axis bars.
      - __First__, this issue needs to be resolved. &#x2192; __*complete*__
  - __Then__, the multi-line (time-machine & forecast requests) __`D3`__ rendered figure will have to be resolved. <u>__*complete*__</u>! (*note the original goal of the project was to produce a time series figure showing both the __historical__ and __forecasted__ temperature data*).


  __2.__ Refactor the `flask_server.py` script such that all the data fetching/parsing will be done with requests to particular *end-points*. <u>__*complete*__</u>

  __3.__ Start constructing the front-end
      - __Update__:
          - The idea is to have a single __*Landing Page*__ which will have links to *different weather parameters that will be rendered by `D3`.
              - The *Landing Page* will have a __search bar__, which will tap into Google Maps' API to auto complete the search when given a query for a city's name (e.g. *Vancouver B.C., Canada*).
              - With the city's name in hand, a call will be made to the Google Maps API to fetch the lat/lon coordinates of that location.
              - Given the location, a request can then be routed to the DarkSky API to retrieve the *hourly* weather data for said location.
      - I'd like to construct data-panels which allows the client to view weather time-series' for a variety of weather parameters, etc.
      - There is also the possibility of doing the above using `React.js`.
          - ...either way, this third step will involve lots more planning and research.

[Back 2 ToC](#toc) &#128070;

## <a id='api'>API requests</a>

### 1. *Forecast* requests
  - URL: `https://api.darksky.net/forecast/[key]/[latitude],[longitude]`
  - *returns the current weather conditions, a __minute-by-minute__ forecast for the __next hour__ (where available), an __hour-by-hour__ forecast for the next 48 hours, and a __day-by-day__ forecast for the next week*.

### 2. *Time-Machine* requests
  - URL: `https://api.darksky.net/forecast/[api-key]/[latitude],[longitude],[time]`
  - *Request returns the observed or forecast weather conditions for a date in the past or future (FOR THE SAKE OF THIS MVP --> FOCUS ON DATES IN THE PAST)*.

[Back 2 ToC](#toc) &#128070;

## <a id='flask-server'>Flask server</a>

  - To run the Flask server, `cd` into `python/flask-d3/` from the projects' root directory.
  - Once there, run `python flask_server.py` to start the server (on `localhost::8080`)
  - __*End-points*__,
    - __`/`__: Index/home page (rendering `templates/index.html`)
      - The `/` end-point currently renders an `<ul>` element, listing `href` links for different parts of the project
        - For example, a listing of temperature parameters links directly to the D3 chart of that weather parameter (<i>i.e.</i> clicking on `Temperature` will take you to a static `html` page for the D3)
    - __`/about`__: Gives a summary of what the project is all about (<i>i.e.</i> what tech stack is used, what API is being used, etc.)
    - __`/temperature`__: Renders the temperature data for *both* the __forecast__ and __time-machine__ requests to the DarkSky API. *Currently, there are some problems encoutered with this end-point (refer to the [question posted on stackoverflow](https://stackoverflow.com/questions/49699408/how-do-i-deal-with-occurrences-of-nan-in-d3?noredirect=1#comment86413836_49699408)), which I'm currently attempting to solve*.
    - __`/forecast`__: Renders the static `D3` `HTML` page, producing a figure of the temperature data returned from a __forecast__ request to the DarkSky API.

[Back 2 ToC](#toc) &#128070;

## <a id='d3'>D3.js charts</a>

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

![multitemp](https://github.com/kdubss/NodeJS-Weather-App/blob/feature/d3/imgs/multitemp.png)

  - From the figure above,
    - Since the data was not rendering properly (despite being successfully passed from server to html), I hard-coded the data into the HTML page to produce this figure. *I'll have to explore the code and read up more, on `D3` to hopefully solve the issue*.

    - __Update__: <u>This has now been solved (*see figure below*)</u>.

![solved](https://github.com/kdubss/NodeJS-Weather-App/blob/master/imgs/combined-temps.png)

  - The issue was in the differences between the y-axis scaling between the historical and frecasted data.  When integer values were input instead of `D3` calls to the data, the time series properly rendered!

![forecast](https://github.com/kdubss/NodeJS-Weather-App/blob/feature/d3/imgs/forecast.png)

  - The weather temperature data returned from the __forecast__ request.



![hindcast](https://github.com/kdubss/NodeJS-Weather-App/blob/feature/d3/imgs/hindcast.png)


  - The weather temperature data returned from the __time-machine__ request.


[Back 2 ToC](#toc) &#128070;

## <a id='data'>Data Parameters</a> (found at *[forecast.io](https://darksky.net)*) - Hourly Data
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
