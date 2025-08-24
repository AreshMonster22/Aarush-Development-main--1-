from flask import Flask, redirect, render_template, request

import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/current", methods=["GET"])
def current():
    location = request.args.get("location", "")
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

@app.route("/forecast", methods=["GET"])
def forecast():
    location = request.args.get("location", "")
    days = request.args.get("days", type=int)
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days={days}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

if __name__ == "__main__":
    app.run()