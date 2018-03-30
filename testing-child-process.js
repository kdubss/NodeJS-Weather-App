// ./weather-app/testing-child-process.js
const { spawn } = require('child_process');
const ls = spawn('ls', ['-lh', './python']);
const runPy = spawn('python', ['./python/test.py']);
const geocodePy = spawn('python', ['./python/geocode.py']);

// runPy.stdout.on('data', (data) => {
//   console.log(`stdout: ${data}`);
// });

geocodePy.stdout.on('data', (data) => {
  console.log(`stdout:\n${data}`);
});
