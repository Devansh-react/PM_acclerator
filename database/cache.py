import json
from datetime import datetime
from sqlalchemy import Table, Column, String, DateTime, MetaData
from database.db import engine

metadata = MetaData()

weather_cache = Table(
    "weather_cache",
    metadata,
    Column("location", String, primary_key=True),
    Column("data", String),
    Column("timestamp", DateTime),
)

# Create table if not exists
metadata.create_all(bind=engine)

def get_weather_cache(location: str):
    with engine.connect() as conn:
        result = conn.execute(
            weather_cache.select().where(weather_cache.c.location == location)
        ).fetchone()
        if result:
            return {"data": json.loads(result.data), "timestamp": result.timestamp}
    return None

def save_weather_cache(location: str, data: dict):
    with engine.connect() as conn:
        conn.execute(
            weather_cache.insert()
            .values(location=location, data=json.dumps(data), timestamp=datetime.now())
            .prefix_with("ON CONFLICT (location) DO UPDATE SET "
                         "data=excluded.data, timestamp=excluded.timestamp")
        )
        conn.commit()
