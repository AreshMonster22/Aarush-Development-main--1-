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
    location = request.args.get("location", "").strip()
    if not location:
        return render_template("index.html", error="Please enter a location.")

    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}"
    r = requests.get(url, timeout=15)
    data = r.json()

    if "error" in data:
        msg = data["error"].get("message", "Could not fetch weather.")
        return render_template("index.html", error=msg)

    loc = data.get("location", {})
    cur = data.get("current", {})

    payload = {
        "location_name": loc.get("name", location),
        "region": loc.get("region", ""),
        "country": loc.get("country", ""),
        "last_updated": cur.get("last_updated", "just now"),
        "temp_c": round(float(cur.get("temp_c", 0))),
        "feelslike_c": round(float(cur.get("feelslike_c", 0))),
        "condition_text": cur.get("condition", {}).get("text", "N/A"),
        "icon_url": ("https:" + cur.get("condition", {}).get("icon", "")) if cur.get("condition") else "",
        "humidity": cur.get("humidity", 0),
        "wind_kph": cur.get("wind_kph", 0),
    }
    return render_template("result.html", **payload)


@app.route("/forecast", methods=["GET"])
def forecast():
    location = request.args.get("location", "")
    days = request.args.get("days", type=int)
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days={days}"
    response = requests.get(url)
    data = json.loads(response.text)
    return render_template("result.html")

if __name__ == "__main__":
    app.run()