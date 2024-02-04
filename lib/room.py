from lib.db import query_db
from models.measurement import Measurement
from models.room import Room

def read_room_temperatures(room_id: int):
    """Get the list of temperatures from a given room"""
    sql = "SELECT * FROM measurements WHERE room_id = %s LIMIT 0, 100"
    cursor = query_db(sql, room_id)
    results = cursor.fetchall()
    data = []
    for row in results:
        item = Measurement(**{
            "id": row[0],
            "temperature": row[1],
            "humidity": row[2],
            "pressure": row[3],
            "created_at": row[4]
        })
        data.append(item)
    return data

def get_room_by_id(room_id: int):
    """Get the data of a single room"""
    sql = "SELECT * FROM rooms WHERE id = %s"
    cursor = query_db(sql, room_id)
    result = cursor.fetchone()
    room = Room(**{
        "id": result[0],
        "name": result[1],
        "label": result[2],
        "created_at": result[3]
    })
    return room

def get_rooms():
    """Get list of rooms"""
    sql = "SELECT * FROM rooms"
    cursor = query_db(sql)
    results = cursor.fetchall()
    data = []
    for row in results:
        item = Measurement(**{
            "id": row[0],
            "temperature": row[1],
            "humidity": row[2],
            "pressure": row[3],
            "created_at": row[4]
        })
        data.append(item)
    return data

def read_last_room_temperature(room_id: int):
    """Read the last temperature for a given room"""
    sql = "SELECT * FROM measurements WHERE room_id = %s ORDER BY created_at DESC LIMIT 1"
    cursor = query_db(sql, room_id)  
    result = cursor.fetchone()
    item = Measurement(**{
        "id": result[0],
        "temperature": result[1],
        "humidity": result[2],
        "pressure": result[3],
        "created_at": result[4]
    })

    return item
