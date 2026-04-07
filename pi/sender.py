# pi/sender.py

import time
import requests
from weather_collector import get_weather_data
from system_collector import get_system_data

API_URL = "https://edge-observability.onrender.com/ingest"

def send(payload):
    if payload is None:
        print("No payload to send, skipping.")
        return
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        print(f"[{payload['source']}] {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[{payload['source']}] Send failed: {e}")

if __name__ == "__main__":
    print("Starting data collection loop...")
    while True:
        send(get_system_data())
        send(get_weather_data())
        print("Sleeping 60 seconds...\n")
        time.sleep(60)
