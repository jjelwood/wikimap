import requests
import json

config = json.load(open("config.json"))

def get_lati_longi(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {

        "address": address,

        "key": config["google_api_key"]

    }

    response = requests.get(url, params=params)

    if response.status_code == 200:

        data = response.json()

        if data["status"] == "OK":

            location = data["results"][0]["geometry"]["location"]

            lat = location["lat"]

            lng = location["lng"]

            return lat, lng

        else:
            print(response)
            print(f"Error: {data['error_message']}")

            return 0, 0

    else:

        print("Failed to make the request." + str(response))

        return 0, 0

def add_coordinates(cursor):
    cursor.execute(f"SELECT name FROM places WHERE latitude IS NULL")
    rows = cursor.fetchall()

    for row in rows:
        place_name = row[0]
        try:
            coordinates = get_lati_longi(place_name)
        except Exception:
            print(f"error with {place_name}")
            continue

        query = f"UPDATE places SET latitude = %s, longitude = %s WHERE name = %s"

        cursor.execute(query, (coordinates[0], coordinates[1], place_name))