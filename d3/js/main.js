// ./weather-app/d3/js/main.js
// Constructing SVG's with D3

// Circle D3
const svg = d3.select('#chart-area')
  .append('svg')
    .attr('width', 400)
    .attr('height', 400)

const circle = svg.append('circle')
  .attr('cx', 100)
  .attr('cy', 250)
  .attr('r', 70)
  .attr('fill', 'grey')

// Rectangle D3:
const svg2 = d3.select('#chart-area-rect')
  .append('svg')
    .attr('width', 500)
    .attr('height', 400)

const rect = svg2.append('rect')
  .attr('x', 0)
  .attr('y', 0)
  .attr('width', 250)
  .attr('height', 100)
  .attr('fill', 'white')
  .attr('')
