import requests
import mysql.connector

def get_api_key():
    with open('key.txt', 'r') as file:
        key = file.read()
        return key

def get_sql_password():
    with open('sql_password.txt', 'r') as file:
        password = file.read()
        return password

def get_lati_longi(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    api_key = get_api_key()
    params = {

        "address": address,

        "key": api_key

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

            print(f"Error: {data['error_message']}")

            return 0, 0

    else:

        print("Failed to make the request.")

        return 0, 0

# address = 'Alcantarilla, Murcia, Spain'
#
# lati, longi = get_lati_longi(address)
#
# print(f"Latitude: {lati}")
#
# print(f"Longitude: {longi}")

#
# Establish the connection
conn = mysql.connector.connect(
    host="127.0.0.1",  # Replace with your host
    user="root",  # Replace with your MySQL username
    password=get_sql_password(),  # Replace with your MySQL password
    database="wikimap_data"  # Replace with your database name
)

# Create a cursor object
cursor = conn.cursor()

# Step 1: Select the value from the identifier column (which is the same as the column to read)
column_to_read = "name"  # Replace with the name of the column you are reading and using as identifier
table_name = "places"  # Replace with your table name
cursor.execute(f"SELECT {column_to_read} FROM {table_name}")

# Fetch all rows
rows = cursor.fetchall()

# Step 2: Loop through each row and update another column using the value read
column_to_update = "coordinates"  # Column where the new value will be inserted


for row in rows:
    value_to_read = row[0]  # Get the value from the column (also the identifier)

    # Perform some logic with the value_to_read
    new_value = str(get_lati_longi(value_to_read))

    # Step 3: Update another column in the same row using the value_to_read as the identifier
    query = f"UPDATE {table_name} SET {column_to_update} = %s WHERE {column_to_read} = %s"

    # Execute the update query with the new value and the same value used as the identifier
    cursor.execute(query, (new_value, value_to_read))

# Commit the transaction to save the changes
conn.commit()

# Print how many rows were updated
print(f"{cursor.rowcount} row(s) updated.")

# Close the connection
cursor.close()
conn.close()