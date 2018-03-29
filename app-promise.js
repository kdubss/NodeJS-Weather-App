const yargs = require('yargs');

const argv = yargs
  .options({
    a: {
      demand: true,
      alias: 'address',
      describe: 'Addresss to fetch weather for (can be a postal/zip code)',
      string: true
    }
  })
  .help()
  .alias('help', 'h')
  .argv;

  
