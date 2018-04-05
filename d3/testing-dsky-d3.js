// ./weather-app/d3/testing-dsky-d3.js
const fname_forecast =  'forecast-hourly-temp.csv';
const path2File = './csv/';

const parseDateTime = d3.timeParse('%Y-%m-%d %H:%M:%S');

d3.csv(path2File + fname_forecast)
  .row((data) => {
    return {
      date: parseDateTime(data.datetime),
      temp: data.temperature
    }
  })
  .get((err, data) => {
    if (err) {
      console.log('\nErrors!\n', err)
    } else {
      console.log(data);

      const minDate = d3.min(data, (d) => { return d.date; });
      const maxDate = d3.max(data, (d) => { return d.date; });

      const minTemp = d3.min(data, (d) => { return d.temp; });
      const maxTemp = d3.max(data, (d) => { return d.temp; });

      console.log('\n----')
      console.log('Min. date range:', minDate);
      console.log('Max. date range:', maxDate);
      console.log('----')
      console.log('Min. temp:', minTemp);
      console.log('Max. temp:', maxTemp);
      console.log('----');

      const svg = d3.select('svg'),
            margin = { top: 20, right: 20, bottom: 30, left: 50 },
            width = +svg.attr('width') - margin.left - margin.right,
            height = +svg.attr('height') - margin.top - margin.bottom,
            g = svg.append('g')
                      .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

      const x = d3.scaleTime()
                  .rangeRound([minDate, maxDate])
                  .domain([minDate, maxDate]);
      const y = d3.scaleLinear()
                  .rangeRound([height, 0])
                  .domain([height, 0])

      console.log('\n----\nx-axis range:', x);
      console.log('y-range:', y, '\n----');

      

    }
  });
