# backend/main.py

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from models import Base, ObservabilityRecord, DataPoint

# --- DATABASE CONNECTION ---
# We read the URL from an environment variable (you'll set this on Render)
# For local testing, you can temporarily hardcode it
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
SessionLocal = sessionmaker(bind=engine)

# Creates the table automatically if it doesn't exist yet
Base.metadata.create_all(bind=engine)

# --- APP ---
app = FastAPI()

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/ingest")
def ingest(data: DataPoint):
    db = SessionLocal()
    try:
        record = ObservabilityRecord(**data.dict())
        db.add(record)
        db.commit()
        return {"status": "stored"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()
