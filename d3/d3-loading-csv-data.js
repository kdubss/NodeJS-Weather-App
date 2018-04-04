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
      const height = 400;
      const width = 600;

      const maxDate = d3.max(data, (d) => { return d.date });
      const minDate = d3.min(data, (d) => { return d.date; });
      const maxTemp = d3.max(data, (d) => { return d.temperature; });
      const minTemp = d3.min(data, (d) => { return d.temperature; });

      console.log('max. Date:', maxDate);
      console.log('min. Date:', minDate);
      console.log('max. Temp:', maxTemp);
      console.log('min. Temp:', minTemp);
    }
  });
