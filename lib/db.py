import pymysql
from lib.conf import getConfig

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