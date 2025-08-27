import json
from datetime import datetime
from sqlalchemy import text
from database.db import engine


def get_weather_cache(location: str):
    """
    Fetch cached weather data for a given location from DB.
    Returns dict with { "data": ..., "timestamp": ... } or None.
    """
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT data, timestamp FROM weather_cache WHERE location = :location"),
            {"location": location},
        ).fetchone()

        if result:
            return {
                "data": json.loads(result.data) if isinstance(result.data, str) else result.data,
                "timestamp": result.timestamp,
            }
        return None


def save_weather_cache(location: str, data: dict):
    """
    Save weather data into cache with UPSERT (Postgres ON CONFLICT).
    """
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO weather_cache (location, data, timestamp)
                VALUES (:location, :data, :timestamp)
                ON CONFLICT (location)
                DO UPDATE SET data = excluded.data, timestamp = excluded.timestamp
            """),
            {
                "location": location,
                "data": json.dumps(data),   # store as JSON
                "timestamp": datetime.now(),
            },
        )
