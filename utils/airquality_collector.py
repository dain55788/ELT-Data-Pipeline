import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()
LOCATION_IDS = os.getenv("LOCATION_ID")
locations = LOCATION_IDS.split()


# FETCH AIR QUALITY DATA BASED ON LOCATION
def fetch_api_openaq(OPENAQ_API_KEY):
    for location in locations:
        url_checkpoint = f"https://api.openaq.org/v3/locations/{location}"
        headers = {"X-API-Key": OPENAQ_API_KEY}
        response = requests.get(url_checkpoint, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching locations for {location}: {response.json()}")
            break
        else:
            data = response.json()
        return data['results']  # just return the 'results' field
