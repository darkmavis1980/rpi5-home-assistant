"""Sensor model module"""
from decimal import Decimal
from pydantic import BaseModel

class Sensor(BaseModel):
    """Sensor Model"""
    temperature: Decimal
    humidity: Decimal
    pressure: Decimal
