# pi/sender.py

import time
import psycopg2
from datetime import datetime, timezone
from weather_collector import get_weather_data
from system_collector import get_system_data

DB_CONFIG = {
    "host": "100.100.21.63",
    "database": "observability",
    "user": "piuser",
    "password": "Lvl_zero",
    "port": 5432
}

def ensure_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS observability (
                id SERIAL PRIMARY KEY,
                timestamp TEXT NOT NULL,
                source TEXT NOT NULL,
                temp_c FLOAT,
                humidity_percent FLOAT,
                weathercode INTEGER,
                cpu_percent FLOAT,
                cpu_load_1m FLOAT,
                memory_percent FLOAT,
                disk_percent FLOAT,
                network_connections INTEGER
            )
        """)
        conn.commit()

def send(payload, conn):
    if payload is None:
        print("No payload to send, skipping.")
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO observability (
                    timestamp, source, temp_c, humidity_percent, weathercode,
                    cpu_percent, cpu_load_1m, memory_percent, disk_percent, network_connections
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                payload.get("timestamp"),
                payload.get("source"),
                payload.get("temp_c"),
                payload.get("humidity_percent"),
                payload.get("weathercode"),
                payload.get("cpu_percent"),
                payload.get("cpu_load_1m"),
                payload.get("memory_percent"),
                payload.get("disk_percent"),
                payload.get("network_connections")
            ))
            conn.commit()
            print(f"[{payload['source']}] stored successfully")
    except Exception as e:
        print(f"[{payload['source']}] Failed: {e}")
        conn.rollback()

if __name__ == "__main__":
    print("Connecting to database...")
    conn = psycopg2.connect(**DB_CONFIG)
    ensure_table(conn)
    print("Starting data collection loop...")
    while True:
        send(get_system_data(), conn)
        send(get_weather_data(), conn)
        print("Sleeping 60 seconds...\n")
        time.sleep(60)
