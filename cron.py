#!/usr/bin/env python

import time
from datetime import datetime
from influxdb_client import Point, WritePrecision
from lib.sensor import Sensor
from lib.db import write_influx_DB, get_db
from lib.conf import get_config

def read_temperature_data():
    config = get_config()

    sensor_type = config.get('SENSOR', 'TYPE')
    print('Sensor type is', sensor_type)
    room_id = config.get('SENSOR', 'ROOM_ID')
    print('Room ID is', room_id)
    sensor = Sensor(sensor_type)

    # Get first reading, which is always wrong
    sensor.get_sensor_reading()
    time.sleep(1)
    sensor.get_sensor_reading()

    # Get DB connection
    connection = get_db()
    try:
        with connection:
            with connection.cursor() as cursor:
                # Get second and correct reading
                sensor.get_sensor_reading()
                temperature = sensor.temperature
                humidity = sensor.humidity
                pressure = sensor.pressure

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
