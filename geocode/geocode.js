const request = require('request');

const geocodeAddress = (address) => {

  const encodedInputAddress = encodeURIComponent(address);

  request({
    url: `https://maps.googleapis.com/maps/api/geocode/json?address=${encodedInputAddress}`,
    json: true
  }, (err, res, body) => {
    if (err) {
      console.log('\nUnable to connect to Google servers!\n');
    } else if (body.status === 'ZERO_RESULTS') {
      console.log('\nUnable to find specified address!\n');
    } else if (body.status === 'OK') {
      console.log(`\nAddress: ${body.results[0].formatted_address}`);
      console.log('---');
      console.log(`Lattitude: ${body.results[0].geometry.location.lat}`);
      console.log(`Longitude: ${body.results[0].geometry.location.lng}`);
      console.log('---\n');
    }
  })

};

module.exports = {
  geocodeAddress
};
