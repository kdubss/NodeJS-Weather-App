// ./weather-app/d3/learn/time-series-line-chart/time-series-line-chart.js
const fname = 'data.tsv';
const parseTime = d3.timeParse('%d-%b-%y');

d3.tsv(fname)
  .row((data) => {
    return {
      date: parseTime(data.date),
      close: +data.close
    }
  })
  .get((err, data) => {
    if (err) {
      console.log('\nErrors:\n', err);
    } else {
      // Setting axis-ranges:
      const minDate = d3.min(data, (d) => { return d.date; });
      const maxDate = d3.max(data, (d) => { return d.date; });

      const minClose = d3.min(data, (d) => { return d.close; });
      const maxClose = d3.max(data, (d) => { return d.close; });

      console.log('Min. date range:', minDate);
      console.log('Max. date range:', maxDate);
      console.log('Min. closing value:', minClose);
      console.log('Max. closing value:', maxClose);

    }
  });
