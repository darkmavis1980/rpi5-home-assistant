#!/usr/bin/env python

import time
from datetime import datetime
from influxdb_client import Point, WritePrecision
from smbus2 import SMBus
from bme280 import BME280
from lib.db import write_influx_DB, get_db
from lib.conf import get_config

# print(
#     """all-values.py - Read temperature, pressure, and humidity
# Press Ctrl+C to exit!
# """
# )

# Initialise the BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

temperature = bme280.get_temperature()
pressure = bme280.get_pressure()
humidity = bme280.get_humidity()


def read_temperature_data():
    """Read the temperature data from the sensor and save it in the databases"""
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    # ignoring first read, as it's always wrong
    time.sleep(1)
    
    room_id = 1

    config = get_config()

    connection = get_db()
    try:
        with connection:
            with connection.cursor() as cursor:
                
                temperature = bme280.get_temperature()
                pressure = bme280.get_pressure()
                humidity = bme280.get_humidity()
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
    except:
        print("Cannot save to the db")

if __name__ == "__main__":
    read_temperature_data()
