
from typing import Literal
from pydantic import BaseModel, Field


class SecurityEventCreate(BaseModel):
    event_type: str = Field(min_length=3, max_length=80)
    severity: Literal["low", "medium", "high", "critical"]
    source: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=500)


class SecurityEvent(SecurityEventCreate):
    id: str
    timestamp: str
