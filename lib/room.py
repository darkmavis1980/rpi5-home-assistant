"""Room functions"""
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
            "id": row.id,
            "temperature": row.temperature,
            "humidity": row.humidity,
            "pressure": row.pressure,
            "created_at": row.created_at,
        })
        data.append(item)
    return data

def get_room_by_id(room_id: int):
    """Get the data of a single room"""
    sql = "SELECT * FROM rooms WHERE id = %s"
    cursor = query_db(sql, room_id)
    result = cursor.fetchone()
    room = {
        "id": result['id'],
        "name": result['name'],
        "label": result['label'],
        "created_at": result['created_at']
    }
    return room

def get_rooms() -> list[Room]:
    """Get list of rooms"""
    sql = "SELECT * FROM rooms"
    cursor = query_db(sql)
    results = cursor.fetchall()
    return results

def read_last_room_temperature(room_id: int) -> Measurement:
    """Read the last temperature for a given room"""
    sql = "SELECT * FROM measurements WHERE room_id = %s ORDER BY created_at DESC LIMIT 1"
    cursor = query_db(sql, room_id)
    result = cursor.fetchone()
    item = Measurement(**{
        "id": result['id'],
        "temperature": result['temperature'],
        "humidity": result['humidity'],
        "pressure": result['pressure'],
        "created_at": result['created_at'],
    })

    return item
