# Weather-App: Node.js, Python/Pandas, D3.js, (React.js)

## Description

  *A CLI weather-tool / (app) which fetches a lat/lon coordinates of user-input address (postal codes, zip codes, cities, etc.), from the Google maps API, and uses those coordinates to fetch the past, current, and forecasted weather data from the forecast.io (darksky.net) API (requires an API-key).  Currently, this only functions as a CLI (command-line-interface) tool, where functionality is run by `Node.js` (e.g. `$node app.js -a [address]`) based on the user-input address*.

  *The* ***goal*** *of this project is to ultimately use `React.js` to create the font-end of an on-line app where* ***current***, ***hourly***, *and* ***minutely*** *weather data will be displayed, both visually as time-series figures and as data tables, depending on the input-address from the user.  Visual representation will be presented by using `D3.js`; Back-end will be powered by `Node.js`; Data fetching, parsing, and manipulations will be done so using `Python/Pandas`*.

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