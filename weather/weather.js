const request = require('request');

const url = 'https://api.darksky.net/forecast/87313e54274f92c50b1c5d843d7471dc/49.2624389,-123.1665417'

const farenheitToCelsius = (temperatureInFarenheit) => {
  const tempInCelsius = (temperatureInFarenheit - 32) * (5/9);
  return tempInCelsius;
};

const getWeather = (lat, lon, callback) => {
  // Want the latitude, longitude, callback(errMsg, res)
  // Takes 2 inputs (an options object), and a callback (in the request() function)
  request({
    url: `https://api.darksky.net/forecast/87313e54274f92c50b1c5d843d7471dc/${lat},${lon}`,
    json: true
  }, (err, res, body) => {
    if (err) {
      callback('\nUnable to connect to the "forecast.io" API!');
    } else if (res.statusCode === 404) {
      callback('\nClient errors - recheck the code in your API request!');
    } else if (res.statusCode === 200) {
      callback(undefined, {
        summary: body.currently.summary,
        temperature_degC: farenheitToCelsius(body.currently.temperature),
        temperature_degF: body.currently.temperature,
        feels_like_degC: farenheitToCelsius(body.currently.apparentTemperature),
        feels_like_degF: body.currently.apparentTemperature,
        rain_probability: body.currently.precipProbability,
        barometric_pressure_mb: body.currently.pressure,
        cloud_cover: body.currently.cloudCover,
        wind_speed_kmh: body.currently.windSpeed,
        wind_gusts_kmh: body.currently.windGust
      });
    }
  });
};

module.exports.getWeather = getWeather;
module.exports.farenheitToCelsius = farenheitToCelsius;
