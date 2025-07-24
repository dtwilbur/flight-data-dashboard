"""CRUD helper functions for interacting with the database.

These functions wrap common patterns for creating and retrieving flights and
positions.  They accept a SQLAlchemy session and Pydantic models as input
and return ORM instances as output.  Separating data access logic into this
module helps keep API route functions clean and testable.
"""

from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List, Optional
from datetime import datetime

from . import models, schemas


def get_flights(db: Session, skip: int = 0, limit: int = 100) -> List[models.Flight]:
    """Return a list of flights from the database."""
    return db.query(models.Flight).offset(skip).limit(limit).all()


def get_flight(db: Session, flight_id: int) -> Optional[models.Flight]:
    """Return a single flight by ID, or None if not found."""
    return db.query(models.Flight).filter(models.Flight.id == flight_id).first()


def create_flight(db: Session, flight: schemas.FlightCreate) -> models.Flight:
    """Create a flight and optionally its positions."""
    db_flight = models.Flight(
        callsign=flight.callsign,
        departure=flight.departure,
        arrival=flight.arrival,
    )
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    # Create positions if provided
    if flight.positions:
        for pos in flight.positions:
            create_position(db, pos, flight_id=db_flight.id)
        # Recalculate first and last seen after positions inserted
        _update_seen_times(db, db_flight)
    return db_flight


def create_position(db: Session, position: schemas.PositionCreate, flight_id: Optional[int] = None) -> models.Position:
    """Create a position entry.  If `flight_id` is provided it will override the one in the schema."""
    fid = flight_id or position.flight_id
    db_position = models.Position(
        flight_id=fid,
        timestamp=position.timestamp,
        latitude=position.latitude,
        longitude=position.longitude,
        altitude=position.altitude,
        speed=position.speed,
        heading=position.heading,
    )
    db.add(db_position)
    # update flight first_seen/last_seen accordingly
    flight = db.query(models.Flight).filter(models.Flight.id == fid).first()
    if flight:
        # update first_seen and last_seen based on the new position
        if not flight.first_seen or position.timestamp < flight.first_seen:
            flight.first_seen = position.timestamp
        if not flight.last_seen or position.timestamp > flight.last_seen:
            flight.last_seen = position.timestamp
    db.commit()
    db.refresh(db_position)
    return db_position


def _update_seen_times(db: Session, flight: models.Flight) -> None:
    """Recompute and update a flight's first_seen and last_seen from its positions."""
    if not flight.positions:
        flight.first_seen = None
        flight.last_seen = None
        return
    timestamps = [pos.timestamp for pos in flight.positions]
    flight.first_seen = min(timestamps)
    flight.last_seen = max(timestamps)
    db.commit()