import pymysql
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from lib.conf import get_config

def get_db():
    """Get the db connection"""
    config = get_config()
    # print('connecting to db {}'.format(config.get('DATABASE', 'HOST')))
    db = pymysql.connect(
        host=config.get('DATABASE', 'HOST'),
        user=config.get('DATABASE', 'USERNAME'),
        passwd=config.get('DATABASE', 'PASSWORD'),
        database=config.get('DATABASE', 'DB'),
    )

    return db

def query_db(sql: str, params = None):
    """Query the database with the passed SQL string"""
    connection = get_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor

def write_influx_DB(data: str):
    """Write data into InfluxDB"""
    config = get_config()
    bucket = config.get('INFLUXDB', 'BUCKET')
    org = config.get('INFLUXDB', 'ORG')
    token = config.get('INFLUXDB', 'TOKEN')
    host = config.get('INFLUXDB', 'HOST')
    with InfluxDBClient(url=host, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        # data = "mem,host=host1 used_percent=23.43234543"
        write_api.write(bucket, org, data)
