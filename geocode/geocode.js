const request = require('request');

const geocodeAddress = (address) => {
  console.log(address);
  const encodedInputAddress = encodeURIComponent(address);
  console.log(encodedInputAddress);

  request({
    url: `https://maps.googleapis.com/maps/api/geocode/json?address=${encodedInputAddress}`,
    json: true
  }, (err, res, body) => {
    if (err) {
      console.log('\nUnable to connect to Google servers!');
    } else if (body.status === 'ZERO_RESULTS') {
      console.log('\nUnable to find specified address!');
    } else if (body.status === 'OK') {
      console.log(`\nAddress: ${body.results[0].formatted_address}`);
      console.log('---');
      console.log(`Lattitude: ${body.results[0].geometry.location.lat}`);
      console.log(`Longitude: ${body.results[0].geometry.location.lng}`);
      console.log('---');
    }
  })
};

geocodeAddress('2703 west 11 avenue vancouver');

module.exports({
  geocodeAddress
});
