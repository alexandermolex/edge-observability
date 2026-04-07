# backend/models.py

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from typing import Optional

# This is the base class all DB table definitions inherit from
Base = declarative_base()

# --- DATABASE TABLE ---
class ObservabilityRecord(Base):
    __tablename__ = "observability"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, nullable=False)
    source = Column(String, nullable=False)  # "weather" or "system"

    # Weather fields (null when source = "system")
    temp_c = Column(Float, nullable=True)
    humidity_percent = Column(Float, nullable=True)
    weathercode = Column(Integer, nullable=True)

    # System fields (null when source = "weather")
    cpu_percent = Column(Float, nullable=True)
    cpu_load_1m = Column(Float, nullable=True)
    memory_percent = Column(Float, nullable=True)
    disk_percent = Column(Float, nullable=True)
    network_connections = Column(Integer, nullable=True)


# --- REQUEST VALIDATION (what the Pi must send) ---
class DataPoint(BaseModel):
    timestamp: str
    source: str

    temp_c: Optional[float] = None
    humidity_percent: Optional[float] = None
    weathercode: Optional[int] = None

    cpu_percent: Optional[float] = None
    cpu_load_1m: Optional[float] = None
    memory_percent: Optional[float] = None
    disk_percent: Optional[float] = None
    network_connections: Optional[int] = None
