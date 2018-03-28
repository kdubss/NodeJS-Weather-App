// const yargs = require('yargs');
//
// const geocode = require('./geocode/geocode');
//
// const argv = yargs
//   .options({
//     a: {
//       demand: true,
//       alias: 'address',
//       describe: 'Set your current address to fetch the weather for.',
//       string: true // always parse the 'a' flag as a string.
//     }
//   })
//   .help()
//   .alias('help', 'h')
//   .argv;
//
// const inputAddress = argv.a;
//
// geocode.geocodeAddress(inputAddress, (err, res) => {
//   if (err) {
//     console.log('\nThere are errors in your request!\n', err, '\n');
//   } else {
//     console.log(JSON.stringify(res, undefined, 2));
//   }
// });
//
// // DarkSky API key: 87313e54274f92c50b1c5d843d7471dc
// // DarkSky API Forecat Request URL: https://api.darksky.net/forecast/[key]/[latitude],[longitude]

// https://api.darksky.net/forecast/87313e54274f92c50b1c5d843d7471dc/49.2624389,-123.1665417

const request = require('request');

const url = 'https://api.darksky.net/forecast/87313e54274f92c50b1c5d843d7471dc/49.2624389,-123.1665417'

const farenheitToCelsius = (temperatureInFarenheit) => {
  const tempInCelsius = (temperatureInFarenheit - 32) * (5/9);
  return tempInCelsius;
};

request({
  url,
  json: true
}, (err, res, body) => {
  if (err) {
    console.log('\nUnable to connect with DarkSky API!\n');
  } else {
    // console.log(body);
    console.log('---');
    console.log('Current temperature in Vancouver is', body.currently.temperature);
  }
});
