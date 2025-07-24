"""SQLAlchemy ORM models for flight and position data.

These classes define the database schema for the flight data application.
Flights are high‑level entities (e.g. a single journey) and contain
metadata such as the callsign and endpoints.  Positions represent individual
time‑stamped telemetry samples for a flight and include latitude, longitude,
altitude and other parameters.
"""

from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Flight(Base):
    """Represents a single flight composed of multiple telemetry samples."""

    __tablename__ = "flights"

    id: int | None = Column(Integer, primary_key=True, index=True)
    callsign: str | None = Column(String, index=True)
    departure: str | None = Column(String, index=True)
    arrival: str | None = Column(String, index=True)
    first_seen: datetime | None = Column(DateTime, index=True)
    last_seen: datetime | None = Column(DateTime, index=True)

    # Define a one‑to‑many relationship to Position.  Cascade deletes ensure
    # positions are removed when a flight is deleted.
    positions = relationship(
        "Position",
        back_populates="flight",
        cascade="all, delete, delete-orphan",
        order_by="Position.timestamp"
    )

    def __repr__(self) -> str:
        return (
            f"<Flight id={self.id} callsign={self.callsign!r} "
            f"departure={self.departure!r} arrival={self.arrival!r}>"
        )


class Position(Base):
    """Represents a single telemetry sample for a flight."""

    __tablename__ = "positions"

    id: int | None = Column(Integer, primary_key=True, index=True)
    flight_id: int | None = Column(Integer, ForeignKey("flights.id"), index=True)
    timestamp: datetime | None = Column(DateTime, index=True)
    latitude: float | None = Column(Float, index=True)
    longitude: float | None = Column(Float, index=True)
    altitude: float | None = Column(Float)
    speed: float | None = Column(Float)
    heading: float | None = Column(Float)

    # Relationship back to Flight
    flight = relationship("Flight", back_populates="positions")

    def __repr__(self) -> str:
        return (
            f"<Position id={self.id} flight_id={self.flight_id} time={self.timestamp} "
            f"lat={self.latitude} lon={self.longitude}>"
        )