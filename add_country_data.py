import pandas as pd
from geopy.geocoders import Nominatim
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
import requests

def get_country(lat, lon):
    try:
        geolocator = Nominatim(user_agent="geoapi")
        location = geolocator.reverse((lat, lon), language="en")
        return location.raw["address"]["country"]
    except Exception as e:
        print(f"Error fetching country for lat: {lat}, lon: {lon} - {e}")
        return None

# Function to get continent from country
def get_continent(country_name):
    try:
        alpha2 = country_name_to_country_alpha2(country_name)
        continent_code = country_alpha2_to_continent_code(alpha2)
        continent_mapping = {
            "AF": "Africa",
            "AS": "Asia",
            "EU": "Europe",
            "NA": "North America",
            "SA": "South America",
            "OC": "Oceania",
            "AN": "Antarctica",
        }
        return continent_mapping.get(continent_code, "Unknown")
    except Exception as e:
        print(f"Error fetching continent for country: {country_name} - {e}")
        return None

def column_exists(cursor, table_name, column_name):
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = %s AND COLUMN_NAME = %s
        """,
        (table_name, column_name),
    )
    return cursor.fetchone()[0] > 0


def add_country_and_continent_to_places(cursor):
    # Check and add columns only if they don't exist
    if not column_exists(cursor, 'places', 'country'):
        cursor.execute("ALTER TABLE places ADD COLUMN country VARCHAR(255)")
    if not column_exists(cursor, 'places', 'continent'):
        cursor.execute("ALTER TABLE places ADD COLUMN continent VARCHAR(255)")

    # Fetch rows with NULL values for country and continent
    cursor.execute("SELECT id, name, latitude, longitude FROM places WHERE country IS NULL AND continent IS NULL")
    rows = cursor.fetchall()

    for row in rows:
        try:
            place_id, name, latitude, longitude = row
            print(f"finding country and continent for: {name}")
            country = get_country(latitude, longitude)
            continent = get_continent(country) if country else None

            # Update the row in the database
            cursor.execute(
                "UPDATE places SET country = %s, continent = %s WHERE id = %s",
                (country, continent, place_id),
            )
        except Exception as e:
            print(f"When attempting to get country and cotinent for place {name} the following error was encountered:\n{e}")


def get_population(country_name):
    # Use RestCountries API with exact match enabled
    api_url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        # Check if data contains a valid population and country name
        if data and isinstance(data, list) and "population" in data[0]:
            population = data[0]["population"]
            print(f"The population of {country_name} is: {population}")
            return population
        else:
            print(f"No valid population found for {country_name}")
            return None
    except Exception as e:
        print(f"Error fetching population for {country_name}: {e}")
        return None


def add_country_data(cursor):
    create_countries_table = """
    CREATE TABLE IF NOT EXISTS countries (
        name VARCHAR(255) PRIMARY KEY,
        population BIGINT DEFAULT NULL
    );
    """
    cursor.execute(create_countries_table)

    # Step 3: Get unique country names from the `places` table and insert them into `countries`
    get_countries_query = """
    SELECT DISTINCT country
    FROM places
    WHERE country IS NOT NULL;
    """
    cursor.execute(get_countries_query)
    countries = cursor.fetchall()

    # Insert countries into the `countries` table
    insert_country_query = "INSERT IGNORE INTO countries (name) VALUES (%s)"
    for country in countries:
        cursor.execute(insert_country_query, (country[0],))

    update_population_query = "UPDATE countries SET population = %s WHERE name = %s"

    for country in countries:
        country_name = country[0]
        population = get_population(country_name)
        if population:
            cursor.execute(update_population_query, (population, country_name))
