const yargs = require('yargs');
const axios = require('axios');

const weather = require('./weather/weather');

const argv = yargs
  .options({
    a: {
      demand: true,
      alias: 'address',
      describe: 'Addresss to fetch weather for (can be a postal/zip code)',
      string: true
    }
  })
  .help()
  .alias('help', 'h')
  .argv;

const encodedInputAddress = encodeURIComponent(argv.address);
const geocodeUrl = `https://maps.googleapis.com/maps/api/geocode/json?address=${encodedInputAddress}`;

// Axios get method --> allows you to make the url request:
// This .get() method returns a Promise!
axios.get(geocodeUrl)
  .then((response) => {
    if (response.data.status === 'ZERO_RESULTS') {
      throw new Error('\nUnable to find specified address!\n');
    }

    const lat = response.data.results[0].geometry.location.lat;
    const lng = response.data.results[0].geometry.location.lng;
    const weatherUrl = `https://api.darksky.net/forecast/87313e54274f92c50b1c5d843d7471dc/${lat},${lng}`
    console.log(response.data.results[0].formatted_address);

    return axios.get(weatherUrl);
  })
  // The following .then() gets called when the weather data is returned from the
  // forecast.io API.
  .then((response) => {
    const temperature = weather.farenheitToCelsius(response.data.currently.temperature);
    const apparentTemperature = weather.farenheitToCelsius(response.data.currently.apparentTemperature);

    console.log(`It's currently ${temperature} deg.C, but it feels like ${apparentTemperature} deg.C`);
  })
  .catch((error) => {
    if (error.code === 'ENOTFOUND') {
      console.log('\nUnable to connect to Google Maps API servers!\n');
    } else {
      console.log(error.message);
    }
  });
