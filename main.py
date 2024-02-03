from typing import Union
from fastapi import FastAPI
from lib.db import getDB, queryDB
import json
from models.measurement import Measurement
from models.room import Room

app = FastAPI()

def getRoom(room_id: int):
    sql = "SELECT * FROM rooms WHERE id = %s"
    cursor = queryDB(sql, room_id)
    result = cursor.fetchone()
    room = Room(**{
        "id": result[0],
        "name": result[1],
        "label": result[2],
        "created_at": result[3]
    })
    return room
    

def readTemperatures(room_id: int):
    sql = "SELECT * FROM measurements WHERE room_id = %s LIMIT 0, 100"
    cursor = queryDB(sql, room_id)
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

def readLastTemperature(room_id: int):
    sql = "SELECT * FROM measurements WHERE room_id = %s ORDER BY created_at DESC LIMIT 1"
    cursor = queryDB(sql, room_id)  
    result = cursor.fetchone()
    item = Measurement(**{
        "id": result[0],
        "temperature": result[1],
        "humidity": result[2],
        "pressure": result[3],
        "created_at": result[4]
    })
    return item

@app.get("/rooms/{room_id}")
def read_root(room_id: int):
    results = readTemperatures(room_id)
    room = getRoom(room_id)
    room.temperatures = results
    return room

@app.get("/rooms/{room_id}/current")
def read_current_temperature(room_id: int):
    temperatures = readLastTemperature(room_id)
    room = getRoom(room_id)
    room.temperatures = temperatures
    return room

@app.post("/rooms/")
def create_room(room: Room):
    pass

@app.put("/rooms/{room_id}")
def update_room(room_id: int, room: Room):
    pass

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}