"""Main application module"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lib.room import get_room_by_id, read_last_room_temperature, read_room_temperatures, get_rooms
from lib.weather import get_forecasts
from models.room import RoomWithTemperature

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/rooms/{room_id}")
def read_room_data(room_id: int):
    """Fetch the data from a room"""
    results = read_room_temperatures(room_id)
    room = get_room_by_id(room_id)
    room.temperatures = results
    return room

@app.get("/rooms/")
def get_list_rooms():
    """Get the list of rooms"""
    results = get_rooms()
    return results

@app.get("/rooms/{room_id}/current")
def read_current_temperature(room_id: int) -> RoomWithTemperature:
    """Fetch the curren temperature from a room"""
    temperatures = read_last_room_temperature(room_id)
    room = get_room_by_id(room_id)

    room['current'] = temperatures
    return room

# @app.post("/rooms/")
# def create_room(room: Room):
#     """Create a new room in the database"""
#     pass

# @app.put("/rooms/{room_id}")
# def update_room(room_id: int, room: Room):
#     """Update an existing room"""
#     pass

@app.get("/forecast")
def get_weather_forecast():
    """Return the current weather forecasts"""
    forecasts = get_forecasts()
    return forecasts

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
