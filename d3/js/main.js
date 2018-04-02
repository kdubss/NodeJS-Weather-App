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
  .attr('width', 200)
  .attr('height', 50)
  .attr('fill', 'white')
  .attr('stroke', 'black')

const ellipse = svg2.append('ellipse')
  .attr('cx', 265)
  .attr('cy', 50)
  .attr('rx', 25)
  .attr('ry', 50)
  .attr('fill', 'blue')

const line = svg2.append('line')
  .attr('x1', 0)
  .attr('y1', 60)
  .attr('x2', 100)
  .attr('y2', 80)
  .attr('color', 'red')
