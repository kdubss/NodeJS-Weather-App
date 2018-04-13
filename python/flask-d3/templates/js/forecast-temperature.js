// ./weather-app/python/js/forecast-temperature.js

// > Forecast data passed from server:
const forecastData = {{ data.forecast_hourly_data | safe }}
console.log('\Forecast data:\n', forecastData)
