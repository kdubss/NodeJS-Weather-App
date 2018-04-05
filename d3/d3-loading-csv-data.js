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

      // console.log('max. Date:', maxDate);
      // console.log('min. Date:', minDate);
      // console.log('max. Temp:', maxTemp);
      // console.log('min. Temp:', minTemp);

      // Defining x,y-scales:
      const y = d3.scaleLinear()
                  .domain([0, maxTemp])
                  .range([height, 0]);
      const x = d3.scaleTime()
                  .domain([minDate, maxDate])
                  .range([0, width]) // width

      // Defining X,Y-Axis:
      const yAxis = d3.axisLeft(y); // defining y-ax with the y-scaling (see above)
      const xAxis = d3.axisBottom(x); // defining the x-ax with the x-scaling (see above)

      

    }
  });
