#!/usr/bin/env python
"""Setup script"""

import os.path
import configparser

FILE_PATH = './conf/conf.ini'

config = configparser.ConfigParser()

def setup_influx_config():
    """Setup the influxDB configuration"""
    influx_host = input('Please enter host: (defaults to localhost)').strip() or 'localhost'
    influx_token = input('Please enter access token:').strip() or ''
    influx_bucket = input('Please enter bucket:').strip() or ''
    influx_org = input('Please enter organization:').strip() or ''
    config.set('INFLUXDB', 'USE_INFLUX', 'yes')
    config.set('INFLUXDB', 'HOST', influx_host)
    config.set('INFLUXDB', 'TOKEN', influx_token)
    config.set('INFLUXDB', 'BUCKET', influx_bucket)
    config.set('INFLUXDB', 'ORG', influx_org)

def setup_redis_config():
    """Setup the Redis configuration"""
    redis_host = input('Please enter host: (defaults to localhost)').strip() or 'localhost'
    redis_port = input('Please enter post: (defaults to 6379)').strip() or '6379'
    redis_password = input('Please enter Redis password:').strip() or ''
    config.set('REDIS', 'USE_REDIS', 'yes')
    config.set('REDIS', 'HOST', redis_host)
    config.set('REDIS', 'PORT', redis_port)
    config.set('REDIS', 'TOKEN', redis_password)

def create_config():
    """Create configuration file"""
    print("Creating MySQL Connection...")
    host = input('Please enter host: (defaults to localhost)').strip() or 'localhost'
    username = input('Please enter username:').strip() or ''
    password = input('Please enter password:').strip() or ''
    db_name = input('Please enter db name:').strip() or ''
    port = input('Please enter port: (defaults to 3306)').strip() or '3306'

    config.add_section('DATABASE')
    config.set('DATABASE', 'HOST', host)
    config.set('DATABASE', 'USERNAME', username)
    config.set('DATABASE', 'PASSWORD', password)
    config.set('DATABASE', 'DB', db_name)
    config.set('DATABASE', 'PORT', port)

    print("Creating sensor configuration")

    room_id = input('Please enter room ID: (defaults to None)').strip() or None
    sensor_type = input('Please enter sensor type: (defaults to BME280)').strip() or 'bme280'
    config.add_section('SENSOR')
    config.set('SENSOR', 'ROOM_ID', room_id)
    config.set('SENSOR', 'TYPE', sensor_type.lower())

    print("Creating InfluxDB Connection...")
    config.add_section('INFLUXDB')

    use_influx = input('Do you want to use InfluxDB? (yes/no)') or 'yes'

    if use_influx.lower() == 'yes':
        setup_influx_config()
    else:
        config.set('INFLUXDB', 'USE_INFLUX', 'no')

    use_redis = input('Do you want to use Redis? (yes/no)') or 'yes'

    if use_redis.lower() == 'yes':
        setup_redis_config()
    else:
        config.set('REDIS', 'USE_REDIS', 'no')

    with open(FILE_PATH, 'w', encoding="utf-8") as configfile:
        config.write(configfile)

if __name__ == "__main__":
    if os.path.isfile(FILE_PATH) is False:
        print('Creating configuration file')
        create_config()
    else:
        print('File already exists')
