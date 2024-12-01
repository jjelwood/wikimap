import csv
import json
import mysql.connector

config = json.load(open('config.json'))

def insert_article(cursor, id, name):
    cursor.execute(
        "INSERT IGNORE INTO articles (id, name, url) VALUES (%s, %s, %s)",
        (id, name, f"https://en.wikipedia.org/wiki/{name}")
    )


class NameGenerator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(file_path, 'r', newline='', encoding="utf8")
        self.reader = csv.DictReader(self.file, delimiter=',')
        self.position = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            row = next(self.reader)
            self.position += 1
            return int(row['Id'][1:]), row['Name']
        except StopIteration:
            self.file.close()
            raise

def export_names(cursor, n, name_generator):
    i = 0
    for (id, name) in name_generator:
        if i >= n:
            break
        print(id, name)
        insert_article(cursor, id, name)
        i += 1

def update_urls(cursor):
    cursor.execute("SELECT id, name FROM articles")
    rows = cursor.fetchall()
    for row in rows:
        id = row[0]
        name = row[1]
        cursor.execute(
            "UPDATE articles SET url = %s WHERE id = %s",
            (f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}", id)
        )