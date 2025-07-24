"""Data ingestion script for satellite telemetry.

This script reads a CSV file containing raw satellite telemetry and loads it
into the database.  Rows should contain at least the following columns:

```
callsign,departure,arrival,timestamp,latitude,longitude,altitude,speed,heading
```

Missing values are allowed for optional fields such as altitude, speed and
heading.  The script will group records by callsign: a new flight is created
whenever a callsign is encountered for the first time.  Subsequent rows for
the same callsign are treated as additional position samples.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import crud, models, schemas


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest satellite flight telemetry into the database")
    parser.add_argument("--csv-file", type=Path, required=True, help="Path to the CSV file containing telemetry data")
    return parser.parse_args()


def init_db() -> None:
    """Create database tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)


def ingest_file(csv_path: Path, db: Session) -> None:
    """Read telemetry from `csv_path` and insert into the database."""
    callsign_to_id: dict[str, int] = {}
    with csv_path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            callsign = row.get("callsign") or None
            departure = row.get("departure") or None
            arrival = row.get("arrival") or None
            ts_str = row.get("timestamp")
            try:
                # parse ISO 8601 or UNIX timestamp
                if ts_str.isdigit():
                    ts = datetime.utcfromtimestamp(float(ts_str))
                else:
                    ts = datetime.fromisoformat(ts_str)
            except Exception:
                print(f"Skipping row with invalid timestamp: {row}")
                continue
            # Determine flight id: create new flight if callsign not seen
            flight_id = callsign_to_id.get(callsign)
            if flight_id is None:
                flight_data = schemas.FlightCreate(
                    callsign=callsign,
                    departure=departure,
                    arrival=arrival,
                    positions=[],
                )
                flight = crud.create_flight(db, flight_data)
                flight_id = flight.id
                callsign_to_id[callsign] = flight_id
            # Create position
            pos_data = schemas.PositionCreate(
                flight_id=flight_id,
                timestamp=ts,
                latitude=float(row.get("latitude")),
                longitude=float(row.get("longitude")),
                altitude=float(row.get("altitude")) if row.get("altitude") else None,
                speed=float(row.get("speed")) if row.get("speed") else None,
                heading=float(row.get("heading")) if row.get("heading") else None,
            )
            crud.create_position(db, pos_data, flight_id=flight_id)


def main() -> None:
    args = parse_arguments()
    init_db()
    # Use dependency generator to get a session
    for db in get_db():
        ingest_file(args.csv_file, db)
        break


if __name__ == "__main__":
    main()