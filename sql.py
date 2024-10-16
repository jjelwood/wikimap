import mysql.connector

# Load database configuration from text file
db_config = {}
with open('database_info.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split('=')
        db_config[key] = value

conn = mysql.connector.connect(
    user=db_config['user'],
    password=db_config['password'],
    host=db_config['host'],
    database=db_config['database']
)

cursor = conn.cursor()