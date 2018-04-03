# ./weather-app/python/flask_server.py
import os
import datetime as dt

from flask import Flask, request, session, flash, render_template, redirect

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':

    app.run(port = 8080)
