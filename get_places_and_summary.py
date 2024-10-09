import requests
import time

def add_places(cursor):
    cursor.execute("SELECT * FROM articles")

    rows = cursor.fetchall()

    for row in rows:
        find_place_id_and_summary(cursor, row)
        time.sleep(0.5)

def find_place_id_and_summary(cursor, row):
    article_id = row[0]
    url = f'https://www.wikidata.org/wiki/Special:EntityData/Q{article_id}.json'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        summary = data['entities'][f'Q{article_id}']['descriptions']['en']['value']
        place_id = data['entities'][f'Q{article_id}']['claims']['P19'][0]['mainsnak']['datavalue']['value']['numeric-id']
        add_place(cursor, place_id)
        add_summary(cursor, article_id, summary)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def add_place(cursor, place_id):
    cursor.execute("INSERT IGNORE INTO places (id) VALUES (%s)", (place_id))

def add_summary(cursor, id, summary):
    cursor.execute("UPDATE articles SET summary = %s WHERE id = %s", (summary, id))
