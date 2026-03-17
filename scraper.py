import requests
import csv
import os
from datetime import datetime, timezone

URL = "https://portalecp.ecp.org.br/servico/servicoconsulta/ConsultaOcupacao"
DATA_FILE = "data/occupancy.csv"

def scrape():
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    payload = response.json()

    # API may return a single object or a list — handle both
    items = payload if isinstance(payload, list) else [payload]
    fitness = next((x for x in items if x.get("descricao") == "Fitness"), None)

    if fitness is None:
        raise ValueError(f"Fitness entry not found. Full response: {payload}")

    total = fitness["total"]
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs("data", exist_ok=True)
    file_exists = os.path.isfile(DATA_FILE)

    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "occupancy"])
        writer.writerow([timestamp, total])

    print(f"[{timestamp}] {total} people in Fitness")

if __name__ == "__main__":
    scrape()
