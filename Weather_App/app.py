from flask import Flask
from datetime import datetime
from flask import render_template
import re
import requests
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
   return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data/")
def get_data():
    kanye_url = requests.get('https://api.kanye.rest')
    quote = kanye_url.json()
    return quote["quote"]

@app.route("/api/weather/<country>")
def get_Weather(country):

    state = get_state(country)
    city = get_city(country, state)
    weather = get_currentWeather(country, state, city)  
    temp = weather['tp']  
    return render_template(
        "weather.html",
        temp=temp,        
    )

def get_state(country):
    URI1 = "https://api.airvisual.com/v2/states?country="+ country +"&key=5eb723fa-d237-479e-a4de-ff5093e1bd2b"
    result1 = requests.get(URI1)
    data1 = result1.json()  
    state = data1['data'][0]['state']
    return state

def get_city(country ,state):
    URI2 = "https://api.airvisual.com/v2/cities?state="+ state +"&country="+ country +"&key=5eb723fa-d237-479e-a4de-ff5093e1bd2b"
    result2 = requests.get(URI2)
    data2 = result2.json()
    city = data2['data'][0]['city']
    return city


def get_currentWeather(country, state, city):
    URI3 = "https://api.airvisual.com/v2/city?city="+city+"&state="+ state +"&country="+ country +"&key=5eb723fa-d237-479e-a4de-ff5093e1bd2b"
    result3 = requests.get(URI3)
    data3 = result3.json()
    weather = data3['data']['current']['weather']
    return weather


  