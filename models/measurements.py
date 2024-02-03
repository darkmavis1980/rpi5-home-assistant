from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

class Measurement(BaseModel):
    id: int
    temperature: Decimal
    humidity: Decimal
    pressure: Decimal
    created_at: datetime