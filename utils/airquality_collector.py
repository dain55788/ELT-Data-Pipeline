import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()
location_id = os.getenv("LOCATION_ID")


# FETCH AIR QUALITY DATA BASED ON LOCATION
def fetch_air_quality_locations(OPENAQ_API_KEY, location_file_path):
    data = None
    url_checkpoint = f"https://api.openaq.org/v3/locations/{location_id}"
    headers = {"X-API-Key": OPENAQ_API_KEY}
    response = requests.get(url_checkpoint, headers=headers)
    data = response.json()

    with open(location_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# FETCH MEASUREMENTS DATA BASED ON SENSORS ACCORDING TO LOCATION
def fetch_air_quality_sensors(OPENAQ_API_KEY, location_file_path, sensor_file_path):
    with open(location_file_path, 'r') as f:
        data = json.load(f)

    # take the sensorid from the sensor field
    sensors = data['results'][0]['sensors']
    sensor_ids = [sensor['id'] for sensor in sensors]

    for sensor in sensor_ids:
        url_checkpoint = f"https://api.openaq.org/v3/sensors/{sensor}"
        headers = {"X-API-Key": OPENAQ_API_KEY}
        response = requests.get(url_checkpoint, headers=headers)
        data = response.json()

        with open(sensor_file_path, 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


# TRANSFORM JSON FORMAT OF SENSOR FILE
def transform_json_format(sensor_file_path):
    combined_results = []

    with open(sensor_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        content = content.replace('}{', '},{')
        content = f'[{content}]'

        data_list = json.loads(content)

        for data in data_list:
            if 'results' in data and isinstance(data['results'], list):
                combined_results.extend(data['results'])

    if sensor_file_path:
        with open(sensor_file_path, 'w', encoding='utf-8') as file:
            json.dump(combined_results, file, indent=4, ensure_ascii=False)
        print(f"Fixed JSON array written to {sensor_file_path}")
