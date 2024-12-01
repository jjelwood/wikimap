import requests
import json
import wikidata_query

config = json.load(open("config.json"))

def get_lati_longi(address, id):
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
            # print(response)
            # print(data)

            return get_lati_longi_wikidata(id)
    else:
        print("Failed to make the request." + str(response))

        return 0, 0

def get_lati_longi_wikidata(id):
    response = wikidata_query.article_query(id)
    try:
        location = response["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]
        print(location)
        return location["latitude"], location["longitude"]
    except KeyError:
        print(f"Location not found for {id}")
        return 0, 0

def add_coordinates(cursor):
    cursor.execute(f"SELECT name, id FROM places WHERE latitude IS NULL")
    rows = cursor.fetchall()

    for row in rows:
        place_name = row[0]
        id = row[1]
        coordinates = get_lati_longi(place_name, id)

        query = f"UPDATE places SET latitude = %s, longitude = %s WHERE name = %s"

        cursor.execute(query, (coordinates[0], coordinates[1], place_name))