#!/usr/bin/env python

import time
from lib.db import getDB, queryDB
from smbus2 import SMBus
from bme280 import BME280

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


def readData():
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    # ignoring first read, as it's always wrong
    time.sleep(1)
    
    connection = getDB()

    with connection:
        with connection.cursor() as cursor:
            
            temperature = bme280.get_temperature()
            pressure = bme280.get_pressure()
            humidity = bme280.get_humidity()
            print(f"{temperature:05.2f}°C {pressure:05.2f}hPa {humidity:05.2f}%")
            sql = "INSERT INTO `measurements` (`temperature`, `humidity`, `pressure`, `room_id`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (temperature, humidity, pressure, 1))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

if __name__ == "__main__":
    readData()
