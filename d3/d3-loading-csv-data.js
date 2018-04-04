// ./weather-app/d3
// - Loading .csv data of the weather data fetched from DarkSky API.

d3.csv('./csv/forecast-hourly-temp.csv')
  .row((data) => {
    return {
      date: data.datetime,
      temperature: +data.temperature
    };
  })
  .get((err, data) => {
    if (err) {
      console.log('\nErrors:\n', err);
    } else {
      console.log(data);
    }
  });
