#!/usr/bin/env python3
"""Weather library"""

import json
import sys
import redis
from lib.conf import get_config

config = get_config()

try:
    import requests
except ImportError:
    sys.exit("This script requires the requests module\nInstall with: sudo pip install requests")

try:
    import geocoder
except ImportError:
    sys.exit("This script requires the geocoder module\nInstall with: sudo pip install geocoder")

# Address
CITY = "Dublin"
COUNTRYCODE = "IE"
WARNING_TEMP = 25.0
# Cache timeout
CACHE_TIMEOUT = 60 * 5

# This maps the weather code from Open Meteo
# to the appropriate weather icons
# Weather codes from https://open-meteo.com/en/docs
icon_map = {
    "snow": [71, 73, 75, 77, 85, 86],
    "rain": [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82],
    "cloud": [1, 2, 3, 45, 48],
    "sun": [0],
    "storm": [95, 96, 99],
    "wind": []
}

"""
Code	Description
0	Clear sky
1, 2, 3	Mainly clear, partly cloudy, and overcast
45, 48	Fog and depositing rime fog
51, 53, 55	Drizzle: Light, moderate, and dense intensity
56, 57	Freezing Drizzle: Light and dense intensity
61, 63, 65	Rain: Slight, moderate and heavy intensity
66, 67	Freezing Rain: Light and heavy intensity
71, 73, 75	Snow fall: Slight, moderate, and heavy intensity
77	Snow grains
80, 81, 82	Rain showers: Slight, moderate, and violent
85, 86	Snow showers slight and heavy
95 *	Thunderstorm: Slight or moderate
96, 99 *	Thunderstorm with slight and heavy hail
"""
icon_map_detailed = {
    "clear": [0],
    "mostly_clear": [1],
    "partly_cloudy": [2],
    "overcast": [3],
    "fog": [45, 48],
    "drizzle": [51, 53, 55],
    "rain_light": [61],
    "rain": [63],
    "rain_heavy": [65],
    "rain_freeze_light": [66],
    "rain_freeze_heavy": [67],
    "snow_light": [71],
    "snow": [73],
    "snow_heavy": [75],
    "hail": [77],
    "rain_shower_light": [80],
    "rain_shower": [81],
    "rain_shower_heavy": [82],
    "thunderstorm": [95],
    "thunderstorm_hail": [96],
    "thunderstorm_hail_heavy": [99],
}

def get_weather_icon(weathercode: int):
    """Get the weather icon"""
    weather_icon = None
    for icon in icon_map:
        if weathercode in icon_map[icon]:
            weather_icon = icon
            break

    return weather_icon

def get_weather_icon_detailed(weathercode: int):
    """Get the weather icon"""
    weather_icon = None
    for icon in icon_map_detailed:
        if weathercode in icon_map_detailed[icon]:
            weather_icon = icon
            break

    return weather_icon

def get_coords(address: str):
    """Convert a city name and country code to latitude and longitude"""
    g = geocoder.arcgis(address)
    coords = g.latlng
    return coords


def get_weather(address: str):
    """Query OpenMeteo (https://open-meteo.com) to get current weather data"""
    coords = get_coords(address)
    weather = {}
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={str(coords[0])}"
            f"&longitude={str(coords[1])}&current_weather=true")
    res = requests.get(url, timeout=2)
    if res.status_code == 200:
        j = json.loads(res.text)
        current = j["current_weather"]
        weather["address"] = address
        weather["temperature"] = current["temperature"]
        weather["windspeed"] = current["windspeed"]
        weather["weathercode"] = current["weathercode"]
        weather["icon"] = get_weather_icon(current["weathercode"])
        weather["icon_detailed"] = get_weather_icon_detailed(current["weathercode"])
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
