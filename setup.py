#!/usr/bin/env python

import os.path

import configparser

filePath = './conf/conf.ini'

def createConfig():
    config = configparser.ConfigParser()

    print("Creating MySQL Connection...")
    host = input('Please enter host: (defaults to localhost)').strip() or 'localhost'
    username = input('Please enter username:').strip() or ''
    password = input('Please enter password:').strip() or ''
    dbName = input('Please enter db name:').strip() or ''
    port = input('Please enter port: (defaults to 3306)').strip() or '3306'

    config.add_section('DATABASE')
    config.set('DATABASE', 'HOST', host)
    config.set('DATABASE', 'USERNAME', username)
    config.set('DATABASE', 'PASSWORD', password)
    config.set('DATABASE', 'DB', dbName)
    config.set('DATABASE', 'PORT', port)

    print("Creating InfluxDB Connection...")
    influx_host = input('Please enter host: (defaults to localhost)').strip() or 'localhost'
    influx_token = input('Please enter access token:').strip() or ''
    influx_bucket = input('Please enter bucket:').strip() or ''
    influx_org = input('Please enter organization:').strip() or ''

    config.add_section('INFLUXDB')
    config.set('INFLUXDB', 'HOST', influx_host)
    config.set('INFLUXDB', 'TOKEN', influx_token)
    config.set('INFLUXDB', 'BUCKET', influx_bucket)
    config.set('INFLUXDB', 'ORG', influx_org)

    with open(filePath, 'w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    if (os.path.isfile(filePath) is False):
        print('Creating configuration file')
        createConfig()
    else:
        print('File already exists')