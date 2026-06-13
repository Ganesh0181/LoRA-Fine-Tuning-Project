import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ORS_API_KEY")

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

url = "https://api.openrouteservice.org/v2/directions/driving-car"

body = {
    "coordinates": [
        [78.4867, 17.3850],   # Hyderabad
        [79.5941, 17.9689]    # Warangal
    ]
}

response = requests.post(
    url,
    json=body,
    headers=headers
)

print(response.status_code)
print(response.json())