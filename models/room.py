"""Room model module"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from models.measurement import Measurement

class Room(BaseModel):
    """Room model"""
    id: int
    name: str
    label: str
    created_at: datetime

class RoomWithTemperature(Room):
    """Room model with temperature fields"""
    temperatures: Optional[List[Measurement]] = None
    current: Optional[Measurement] = None
