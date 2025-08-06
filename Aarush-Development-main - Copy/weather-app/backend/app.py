from flask import Flask, request, redirect, render_template

import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to the ProWeather App"

@app.route("/WeatherAPI", methods=["GET"])
def WeatherAPI():
    location = request.args.get("location", "")
    days = request.args.get("days", type=int)
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days={days}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

if __name__ == "__main__":
    app.run()