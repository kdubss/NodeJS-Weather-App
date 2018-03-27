const yargs = require('yargs');

const geocode = require('./geocode/geocode');

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

geocode.geocodeAddress(argv.a);

const encodedUserAddress = encodeURIComponent(argv.a);

request({
  url: `https://maps.googleapis.com/maps/api/geocode/json?address=${encodedUserAddress}`,
  json: true
}, (err, res, body) => {
  if (err) {
    console.log('\nUnable to connect to Google servers.\n');
  } else if (body.status === 'ZERO_RESULTS') {
    console.log('\nUnable to find the specified address!\n');
  } else if (body.status === 'OK') {
    console.log(`\nAddress: ${body.results[0].formatted_address}`);
    console.log(`\nLatitutde: ${body.results[0].geometry.location.lat}`);
    console.log(`Longitude: ${body.results[0].geometry.location.lng}\n`);
  }
});
