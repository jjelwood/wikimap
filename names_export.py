import csv
import mysql.connector

def insert_article(cursor, id, name):
    cursor.execute(
        "INSERT IGNORE INTO articles (id, name, url) VALUES (%s, %s, %s)",
        (id, name, f"https://en.wikipedia.org/wiki/{name}")
    )

def export_names(cursor, path):
    with open(path, 'r', newline='', encoding="utf8") as f:
        reader = csv.DictReader(f, delimiter=',')
        count = 0
        for row in reader:
            if count >= 5000:
                break
            id = int(row['Id'][1:])
            name = row['Name']
            print(id, name)
            insert_article(cursor, id, name)
            count += 1
        f.close()