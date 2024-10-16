import requests
import time

def add_places(cursor):
    cursor.execute("SELECT * FROM articles")

    rows = cursor.fetchall()

    for row in rows:
        if row[2] is not None and row[3] is not None:
            continue
        make_query(cursor, row)

def article_query(article_id):
    url = f'https://www.wikidata.org/wiki/Special:EntityData/Q{article_id}.json'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['entities'][f'Q{article_id}']

def get_places_and_summaries(cursor, row):
    article_id = row[0]
    
    try:
        article_data = article_query(article_id)

        # Update the article with the summary
        summary = article_data['descriptions']['en']['value']
        cursor.execute("UPDATE articles SET summary = %s WHERE id = %s AND summary IS NULL", (summary, article_id))

        # Update the article with the place ID, and add the place to the places table
        place_id = article_data['claims']['P19'][0]['mainsnak']['datavalue']['value']['numeric-id']
        cursor.execute("INSERT IGNORE INTO places (id) VALUES (%s)", (place_id,))
        cursor.execute("UPDATE articles SET place_id = %s WHERE id = %s AND place_id IS NULL", (place_id, article_id))

        # Log the result
        print(f"Article ID: {article_id}, Place ID: {place_id}, Summary: {summary}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except KeyError as e:
        print(f"Article ID: {article_id}, Key error: {e}")

def populate_places(cursor):
    cursor.execute("SELECT id FROM places WHERE name IS NULL")

    rows = cursor.fetchall()

    for row in rows:
        id = row[0]
        place_data = article_query(id)
        name = place_data['labels']['en']['value']
        print(name)
        cursor.execute("UPDATE places SET name = %s WHERE id = %s", (name, id))


