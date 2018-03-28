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

const inputAddress = argv.a;

geocode.geocodeAddress(inputAddress, (err, res) => {
  if (err) {
    console.log('\nThere are errors in your request!\n', err, '\n');
  } else {
    console.log(JSON.stringify(res, undefined, 2));
  }
});
