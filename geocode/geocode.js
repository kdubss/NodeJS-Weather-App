const request = require('request');

const geocodeAddress = (address, callback) => {

  const encodedInputAddress = encodeURIComponent(address);

  request({
    url: `https://maps.googleapis.com/maps/api/geocode/json?address=${encodedInputAddress}`,
    json: true
  }, (err, res, body) => {
    if (err) {
      callback('\nUnable to connect to Google servers!\n')
    } else if (body.status === 'ZERO_RESULTS') {
      callback('\nUnable to find specified address!\n');
    } else if (body.status === 'OK') {
      callback(undefined, {
        address: body.results[0].formatted_address,
        latitude: body.results[0].geometry.location.lat,
        longitude: body.results[0].geometry.location.lng
      });
    }
  });

};

module.exports.geocodeAddress = geocodeAddress;
