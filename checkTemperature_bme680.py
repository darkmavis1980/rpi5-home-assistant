#!/usr/bin/env python

import time
from datetime import datetime
from influxdb_client import Point, WritePrecision
from smbus2 import SMBus
import bme680
from lib.db import write_influx_DB, get_db
from lib.conf import get_config

# print(
#     """all-values.py - Read temperature, pressure, and humidity
# Press Ctrl+C to exit!
# """
# )

# Initialise the BME680
try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)


def read_temperature_data():
    """Read the temperature data from the sensor and save it in the databases"""
    temperature = sensor.data.temperature
    pressure = sensor.data.pressure
    humidity = sensor.data.humidity
    # ignoring first read, as it's always wrong
    time.sleep(1)
    
    room_id = 2  

    config = get_config()

    connection = get_db()
    try:
        with connection:
            with connection.cursor() as cursor:            
                temperature = sensor.data.temperature
                pressure = sensor.data.pressure
                humidity = sensor.data.humidity
                print(f"{temperature:05.2f}°C {pressure:05.2f}hPa {humidity:05.2f}%")
                sql = "INSERT INTO `measurements` (`temperature`, `humidity`, `pressure`, `room_id`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (temperature, humidity, pressure, room_id))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            if config.get('INFLUXDB', 'USE_INFLUX') == 'yes':
                point = Point("room") \
                    .tag("roomId", room_id) \
                    .field("temperature", temperature) \
                    .field("pressure", pressure) \
                    .field("humidity", humidity) \
                    .time(datetime.utcnow(), WritePrecision.NS)
                write_influx_DB(point)
    except Exception as e:
        print(e)
        print("Cannot save to the db")

if __name__ == "__main__":
    read_temperature_data()
