// ./weather-app/testing-child-process.js
const { spawn } = require('child_process');
const ls = spawn('ls', ['-lh', './python']);
const runPy = spawn('python', ['./python/test.py']);

runPy.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});
