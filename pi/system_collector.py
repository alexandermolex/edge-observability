# pi/system_collector.py

import psutil
from datetime import datetime, timezone

def get_system_data():
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "system",
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_load_1m": psutil.getloadavg()[0],
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "network_connections": len(psutil.net_connections())
    }
    return payload

if __name__ == "__main__":
    import json
    print(json.dumps(get_system_data(), indent=2))
