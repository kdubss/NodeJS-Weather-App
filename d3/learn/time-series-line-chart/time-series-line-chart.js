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

      const svg = d3.select('svg'),
            margin = {top: 20, right: 20, bottom: 30, left: 50},
            width = +svg.attr('width') - margin.left - margin.right,
            height = +svg.attr('height') - margin.top - margin.bottom,
            g = svg.append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

      // x & y both returns a 'Scale' function
      const x = d3.scaleTime()
                  .rangeRound([0, width])
                  .domain([minDate, maxDate]);
      const y = d3.scaleLinear()
                  .rangeRound([height, 0])
                  .domain([height, 0]);

      console.log('\n---', '\nBoth \'x\' and \'y\' returns a scale() function in D3\n');
      console.log('X scale:', x);
      console.log('Y scale:', y);
      console.log('---\n');

      const line = d3.line()
                     .x((d) => { return x(d.date); })
                     .y((d) => { return y(d.close); });

      console.log('Line object:', line);
      console.log('Returns a line() function, which is a spline or polyline.');
      console.log('The line(data) generates a line for a given array of data.\n\
Depending on the lin generators associated curve, the given input data may be \
needed to be sorted by the x-value (i.e. the dates should be arranged chronologically?)');
      console.log('---\n');

      console.log('g:', g, '\n');
      console.log('d3.axisBottom(x):', d3.axisBottom(x));
      console.log('\nCalling \'d3.axisBottom(x)\' will return an \'Axes\' d3 \
module, which in this case, are human-readable reference marks for scales!');
      console.log('---\n');

      g.append('g')
          .attr('transform', 'translate(0,' + height + ')')
          .call(d3.axisBottom(x))
        .select('.domain')
          .remove();

      g.append('g')
          .call(d3.axisLeft(y))
        .append('text')
          .attr('fill', '#000')
          .attr('transform', 'rotate(-90)')
          .attr('y', 6)
          .attr('dy', '0.71em')
          .text('price ($)');


    }
  });
