"""Pydantic schemas for input validation and serialisation.

Pydantic models are used by FastAPI to validate request bodies and serialise
responses.  The `orm_mode` configuration tells Pydantic to read data from
SQLAlchemy model instances directly.【659874306774395†L315-L328】
"""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


class PositionBase(BaseModel):
    timestamp: datetime = Field(..., description="UTC timestamp of the sample")
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in degrees")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude in degrees")
    altitude: Optional[float] = Field(None, description="Altitude in metres")
    speed: Optional[float] = Field(None, description="Ground speed in knots")
    heading: Optional[float] = Field(None, description="Heading in degrees")


class PositionCreate(PositionBase):
    flight_id: int = Field(..., description="ID of the flight this position belongs to")


class Position(PositionBase):
    id: int
    flight_id: int

    class Config:
        orm_mode = True


class FlightBase(BaseModel):
    callsign: Optional[str] = Field(None, description="Unique callsign or tail number")
    departure: Optional[str] = Field(None, description="Departure airport code")
    arrival: Optional[str] = Field(None, description="Arrival airport code")


class FlightCreate(FlightBase):
    # When creating a flight via API, positions can optionally be supplied
    positions: Optional[List[PositionCreate]] = None


class FlightSummary(FlightBase):
    id: int
    first_seen: Optional[datetime]
    last_seen: Optional[datetime]

    class Config:
        orm_mode = True


class Flight(FlightSummary):
    positions: List[Position] = []

    class Config:
        orm_mode = True