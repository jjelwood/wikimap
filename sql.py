import mysql.connector
import json

# Load database configuration from text file
config = json.load(open('config.json'))

conn = mysql.connector.connect(
    user=config['sqluser'],
    password=config['sqlpassword'],
    host=config['sqlhost']
)

cursor = conn.cursor(buffered=True)