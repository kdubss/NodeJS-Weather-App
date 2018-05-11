const yargs = require('yargs');
const express = require('express');
const PORT = process.env.PORT || 8080;

const app = express();

const geocode = require('./geocode/geocode');
const weather = require('./weather/weather');

app.get('/', (req, res) => {
  res.send('Index Page');
});

app.get('/local', (req, res) => {
  res.send('Current Local Weather');
});

app.listen(PORT, () => {
  console.log(`\nDark Sky Weather now running on LOCAL PORT ${PORT}!`);
});
