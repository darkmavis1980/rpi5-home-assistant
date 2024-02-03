from pydantic import BaseModel
from typing import Union, Optional, List
from models.measurement import Measurement

class Room(BaseModel):
    id: int
    name: str
    label: str
    temperatures: Optional[List[Measurement]] = None
    current: Optional[Measurement] = None
