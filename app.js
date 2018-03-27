const request = require('request');

request({
  url: 'https://maps.googleapis.com/maps/api/geocode/json?address=2703%20west%2011%20avenue%20vancouver',
  json: true
}, (err, res, body) => {
  if (err) {
    console.error();
  } else {
    console.log('Printing "body"\n', JSON.stringify(body, undefined, 2));
  }
});
