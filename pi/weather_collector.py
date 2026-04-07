# pi/weather_collector.py

import requests
from datetime import datetime, timezone

def get_weather_data():
    latitude = 42.3
    longitude = -83.0  # Detroit area

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,weathercode",
        "timezone": "auto"
    }

    response = requests.get(url, params=params, timeout=10)
    
    if response.status_code != 200:
        print(f"Weather API error: {response.status_code}")
        return None

    data = response.json()
    current = data.get("current", {})

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "weather",
        "temp_c": current.get("temperature_2m"),
        "humidity_percent": current.get("relative_humidity_2m"),
        "weathercode": current.get("weathercode")
    }

    return payload

if __name__ == "__main__":
    import json
    result = get_weather_data()
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("No data returned — try again in a moment")
