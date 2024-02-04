import pymysql
from lib.conf import getConfig
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def getDB():
    config = getConfig()
    # print('connecting to db {}'.format(config.get('DATABASE', 'HOST')))
    db = pymysql.connect(
        host=config.get('DATABASE', 'HOST'),
        user=config.get('DATABASE', 'USERNAME'),
        passwd=config.get('DATABASE', 'PASSWORD'),
        database=config.get('DATABASE', 'DB'),
    )

    return db

def queryDB(sql: str, params = None):
    connection = getDB()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor

def writeInfluxDB(data: str):
    config = getConfig()
    bucket = config.get('INFLUXDB', 'BUCKET')
    org = config.get('INFLUXDB', 'ORG')
    token = config.get('INFLUXDB', 'TOKEN')
    host = config.get('INFLUXDB', 'HOST')
    with InfluxDBClient(url=host, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        # data = "mem,host=host1 used_percent=23.43234543"
        write_api.write(bucket, org, data)
