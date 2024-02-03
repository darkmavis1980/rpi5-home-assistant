from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

class Measurement(BaseModel):
    id: int
    temperature: Decimal
    humidity: Decimal
    pressure: Decimal
    created_at: datetime
    # room_id: Optional[int] = None