#!/usr/bin/env python3

import json
import redis
from lib.conf import get_config

config = get_config()

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
CACHE_TIMEOUT = 60 * 5

def get_coords(address: str):
    """Convert a city name and country code to latitude and longitude"""
    g = geocoder.arcgis(address)
    coords = g.latlng
    return coords


def get_weather(address: str):
    """Query OpenMeteo (https://open-meteo.com) to get current weather data"""
    coords = get_coords(address)
    weather = {}
    url = f"https://api.open-meteo.com/v1/forecast?latitude={str(coords[0])}&longitude={str(coords[1])}&current_weather=true"
    res = requests.get(url, timeout=2)
    if res.status_code == 200:
        j = json.loads(res.text)
        current = j["current_weather"]
        weather["address"] = address
        weather["temperature"] = current["temperature"]
        weather["windspeed"] = current["windspeed"]
        weather["weathercode"] = current["weathercode"]
        return weather
    else:
        return weather

def get_forecasts():
    """Get the forecast with the current address"""
    has_redis = False

    if config.get('REDIS', 'USE_REDIS') == 'yes':
        has_redis = True
        host = config.get('REDIS', 'HOST') or 'localhost'
        port = config.get('REDIS', 'PORT') or 6379
        redis_password = config.get('REDIS', 'PASSWORD') or ''
        print(host, port, redis_password)
        r = redis.Redis(host=host, port=port, password=redis_password, decode_responses=True)

        data = r.get('forecast')
        if data is not None:
            print('Fetching data from cache')
            return json.loads(data)

    location_string = f"{CITY}, {COUNTRYCODE}"
    weather = get_weather(location_string)
    if has_redis is True:
        print('Cache not set, writing to it')
        r.set('forecast', json.dumps(weather), ex=CACHE_TIMEOUT)
    return weather
