"""FastAPI application entry point.

This module defines the API routes for the flight data service.  The API
supports creating flights and positions, listing flights and retrieving
detailed information.  CORS is configured to allow requests from the local
frontend during development.
"""

from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from . import crud, models, schemas
from .database import Base, engine, get_db


# Create database tables on startup.  In production you might prefer Alembic
# migrations instead of calling `create_all` at runtime.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flight Data API", description="API for ingesting and visualising flight telemetry.")

# Allow CORS during development.  Restrict origins in production.
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/flights", response_model=List[schemas.FlightSummary])
def read_flights(skip: int = 0, limit: int = Query(100, le=1000), db: Session = Depends(get_db)):
    """Return a paginated list of flights."""
    flights = crud.get_flights(db, skip=skip, limit=limit)
    return flights


@app.get("/flights/{flight_id}", response_model=schemas.Flight)
def read_flight(flight_id: int, db: Session = Depends(get_db)):
    """Return details and positions for a single flight."""
    flight = crud.get_flight(db, flight_id=flight_id)
    if flight is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight


@app.post("/flights", response_model=schemas.Flight, status_code=201)
def create_flight(flight: schemas.FlightCreate, db: Session = Depends(get_db)):
    """Create a new flight with optional positions."""
    return crud.create_flight(db, flight)


@app.post("/positions", response_model=schemas.Position, status_code=201)
def create_position(position: schemas.PositionCreate, db: Session = Depends(get_db)):
    """Create a new position sample for an existing flight."""
    # Ensure the flight exists
    flight = crud.get_flight(db, position.flight_id)
    if flight is None:
        raise HTTPException(status_code=400, detail="Flight does not exist")
    return crud.create_position(db, position)


@app.get("/positions/latest", response_model=List[schemas.Position])
def read_latest_positions(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    """Return the most recent position sample for each flight.

    The endpoint returns at most `limit` entries ordered by timestamp descending.
    """
    # Query the latest positions across flights
    subquery = (
        db.query(models.Position.flight_id, models.Position.timestamp)
        .order_by(models.Position.flight_id, models.Position.timestamp.desc())
        .distinct(models.Position.flight_id)
        .subquery()
    )
    query = (
        db.query(models.Position)
        .join(
            subquery,
            (models.Position.flight_id == subquery.c.flight_id)
            & (models.Position.timestamp == subquery.c.timestamp),
        )
        .order_by(models.Position.timestamp.desc())
        .limit(limit)
    )
    return query.all()