const yargs = require('yargs');

const geocode = require('./geocode/geocode');
const weather = require('./weather/weather');

const argv = yargs
  .options({
    a: {
      demand: true,
      alias: 'address',
      describe: 'Set your current address to fetch the weather for.',
      string: true // always parse the 'a' flag as a string.
    }
  })
  .help()
  .alias('help', 'h')
  .argv;

const inputAddress = argv.a;

geocode.geocodeAddress(inputAddress, (err, geoRes) => {

  if (err) {
    console.log('\nThere are errors in your request!\n', err, '\n');
  } else {
    console.log(`\n${geoRes.address}`);
    weather.getWeather(geoRes.latitude, geoRes.longitude, (err, weatherRes) => {
      // The callback function will get fired when the 'res' data is returned from
      // the forecast.io API!
      if (err) {
        console.log('\nThere are errors in your current request!\n', err, '\n');
      } else {
        console.log('\nWeather data fetched from \'forecast.io\' (aka darksky.net)');
        console.log(`\nWeather summary for ${inputAddress}`);
        console.log(`  - It\'s currently ${weatherRes.temperature_degC} but feels like ${weatherRes.feels_like_degC}`);
        console.log(`  - The current condition is ${weatherRes.summary}\n`);
        console.log('----');
        console.log(JSON.stringify(weatherRes, undefined, 2));
        console.log('----\n');
      }
    })
  }

});
