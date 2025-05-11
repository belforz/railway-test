from pydantic import BaseModel
from datetime import datetime

class InteractionModel(BaseModel):
    message: str
    response: str
    timestamp: datetime
