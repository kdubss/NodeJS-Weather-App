const yargs = require('yargs');
const express = require('express');
const PORT = process.env.PORT || 8080;

const app = express();

const geocode = require('./geocode/geocode');
const weather = require('./weather/weather');

app.listen(PORT, () => {
  console.log(`\nDark Sky Weather now running on LOCAL PORT ${PORT}!`);
});
