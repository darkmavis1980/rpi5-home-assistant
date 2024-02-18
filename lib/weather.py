#!/usr/bin/env python3

import json

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

try:
    import geocoder
except ImportError:
    exit("This script requires the geocoder module\nInstall with: sudo pip install geocoder")

CITY = "Dublin"
COUNTRYCODE = "IE"
WARNING_TEMP = 25.0

def get_coords(address: str):
    """Convert a city name and country code to latitude and longitude"""
    g = geocoder.arcgis(address)
    coords = g.latlng
    return coords


def get_weather(address: str):
    """Query OpenMeteo (https://open-meteo.com) to get current weather data"""
    coords = get_coords(address)
    weather = {}
    res = requests.get("https://api.open-meteo.com/v1/forecast?latitude=" + str(coords[0]) + "&longitude=" + str(coords[1]) + "&current_weather=true")
    if res.status_code == 200:
        j = json.loads(res.text)
        current = j["current_weather"]
        weather["temperature"] = current["temperature"]
        weather["windspeed"] = current["windspeed"]
        weather["weathercode"] = current["weathercode"]
        return weather
    else:
        return weather

def get_forecasts():
    """Get the forecast with the current address"""
    location_string = f"{CITY}, {COUNTRYCODE}"
    weather = get_weather(location_string)
    return weather
