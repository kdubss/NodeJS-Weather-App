const request = require('request');

request({
  url: 'https://maps.googleapis.com/maps/api/geocode/json?address=2703%20west%2011%20avenue%20vancouver',
  json: true
}, (err, res, body) => {
  if (err) {
    console.error('Errors:\n', JSON.stringify(err, undefined, 2));
  } else {
    // console.log('Printing request "body"\n', JSON.stringify(res, undefined, 2));
    console.log(`Address: ${body.results[0].formatted_address}`);
    console.log(`\nLatitutde: ${body.results[0].geometry.location.lat}`);
    console.log(`Longitude: ${body.results[0].geometry.location.lng}`);
  }
});
