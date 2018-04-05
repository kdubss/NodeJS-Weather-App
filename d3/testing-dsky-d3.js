// ./weather-app/d3/testing-dsky-d3.js
const fname_forecast =  'forecast-hourly-temp.csv';
const path2File = './csv/';

const parseDateTime = d3.timeParse('%Y-%m-%d %H:%M:%S');

d3.csv(path2File + fname_forecast)
  .row((data) => {
    return {
      date: parseDateTime(data.date),
      temp: data.temperature
    }
  })
  .get((err, data) => {
    if (err) {
      console.log('\nErrors!\n', err)
    } else {
      console.log(data);
    }
  });
