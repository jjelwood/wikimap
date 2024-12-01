import datetime
import requests

def add_places_summaries_and_birthdates(cursor):
    cursor.execute("SELECT * FROM articles")

    rows = cursor.fetchall()

    for row in rows:
        get_places_and_summaries_and_birthdates(cursor, row)

def article_query(article_id):
    url = f'https://www.wikidata.org/wiki/Special:EntityData/Q{article_id}.json'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['entities'][f'Q{article_id}']

def convert_datetime(dt_str):
    try:
        print(dt_str)
        parts = list(map(int,dt_str.split("T")[0].split("-")))
        year = parts[0]
        month = parts[1] if parts[1] != 0 else 1
        day = parts[2] if parts[2] != 0 else 1
        date = datetime.datetime(year, month, day)
        print(date)
        # Format the datetime to MySQL format
        return date.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError) as e:
        # Handle incorrect datetime format
        print(f"Invalid datetime format: {dt_str} - {e}")
        return None

def get_wikipedia_title_from_wikidata_id(wikidata_id):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/Q{wikidata_id}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        entities = data.get('entities', {})
        entity = entities.get(f"Q{wikidata_id}", {})
        sitelinks = entity.get('sitelinks', {})
        enwiki = sitelinks.get('enwiki', {})
        title = enwiki.get('title', None)
        print(title)
        return title
    else:
        print(f"Failed to resolve Wikidata ID: {response.text}")
        return None

def update_wikipedia_titles(cursor):
    cursor.execute("SELECT id, name FROM articles")

    rows = cursor.fetchall()

    for row in rows:
        id = row[0]
        name = row[1]
        title = get_wikipedia_title_from_wikidata_id(id)
        if title:
            if name != title:
                print(f"Updating {id} from {name} to {title}")
                cursor.execute("UPDATE articles SET name = %s WHERE id = %s", (title, id))
            else:
                print(f"{id} already has the correct title")
        else:
            print(f"Failed to resolve Wikipedia title for {id}")

def get_places_and_summaries_and_birthdates(cursor, row):
    article_id = row[0]

    cursor.execute("SELECT summary FROM articles WHERE id = %s", (article_id,))
    result = cursor.fetchone()
    if result and result[0] is not None:
        return
    
    try:
        article_data = article_query(article_id)

        # Update the article with the summary
        summary = article_data['descriptions']['en']['value']
        cursor.execute("UPDATE articles SET summary = %s WHERE id = %s AND summary IS NULL", (summary, article_id))

        datestring = article_data['claims']['P569'][0]['mainsnak']['datavalue']['value']['time']
        birthdate = convert_datetime(datestring[1 if datestring.startswith("+") else 0:-1])
        cursor.execute("UPDATE articles SET date = %s WHERE id = %s AND date IS NULL", (birthdate, article_id))
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except KeyError as e:
        print(f"Article ID: {article_id}, Birthdate not found: {e}")
    except Exception as e:
        print(f"Article ID: {article_id}, Error: {e}")
    
    try:
        # Update the article with the place ID, and add the place to the places table
        place_id = article_data['claims']['P19'][0]['mainsnak']['datavalue']['value']['numeric-id']
        cursor.execute("INSERT IGNORE INTO places (id) VALUES (%s)", (place_id,))
        cursor.execute("UPDATE articles SET place_id = %s WHERE id = %s AND place_id IS NULL", (place_id, article_id))
    except KeyError as e:
        cursor.execute("UPDATE articles SET place_id = %s WHERE id = %s", (-1, article_id))
        print(f"Article ID: {article_id}, Place ID not found: {e}")
    
    # print(f"Article ID: {article_id}, Place ID: {place_id}, Birthdate: {birthdate}, Summary: {summary}")

def populate_places(cursor):
    cursor.execute("SELECT id FROM places WHERE name IS NULL")

    rows = cursor.fetchall()

    for row in rows:
        id = row[0]
        place_data = article_query(id)
        languages = place_data['labels'].keys()
        if 'en' not in languages:
            name = place_data['labels'][list(languages)[0]]['value']
        else:
            name = place_data['labels']['en']['value']
        print(name)
        cursor.execute("UPDATE places SET name = %s WHERE id = %s", (name, id))


