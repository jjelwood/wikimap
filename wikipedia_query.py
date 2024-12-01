#this file retrieves the internal links of different article names
import requests

S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php" # general api url link
URL_REST = "https://en.wikipedia.org/api/rest_v1/page/" # rest api url link

def query_wikipedia(title, prop):
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": prop,
        # "rvprop": "user",
        # "rvlimit": 1 if prop != "revisions" else "max",
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    PAGES = DATA["query"]["pages"]

    return PAGES

def get_links(cursor):
    # for each article, based on its title, use the active session to fetch via the wikipedia api the internal links titles

    cursor.execute("SELECT id, name FROM articles")

    for row in cursor.fetchall():
        id = row[0]
        title = row[1]
        results = query_wikipedia(title, "links")
        print(f"Finding links in {title}")

        for k, v in results.items():
            if "links" not in v:
                for l in v["links"]:
                    cursor.execute("SELECT id FROM articles WHERE name = %s", (l["title"],))
                    result = cursor.fetchone()
                    if result and result[0] != id:
                        print(id, title, result[0], l["title"])
                        cursor.execute(
                            "INSERT INTO links (from_id, from_name, to_id, to_name) VALUES (%s, %s, %s, %s)",
                            (id, title, result[0], l["title"])
                        )
                break
        else:
            print(f"Failed to get links for {title}")

def get_lengths(cursor):
    # for each article, based on its title, use the active session to fetch via the wikipedia api the length of the article

    cursor.execute("SELECT id, name FROM articles WHERE length IS NULL")
    rows = cursor.fetchall()

    for i, row in enumerate(rows):
        id = row[0]
        title = row[1]
        results = query_wikipedia(title, "info")

        for k, v in results.items():
            if "length" in v:
                if type(v["length"]) == int:
                    length = v["length"]
                else:
                    length = v[id]["length"]
                print(f"{i+1}/{len(rows)}; {title} is {length} characters long")
                cursor.execute("UPDATE articles SET length = %s WHERE id = %s", (length, id))
                break
        else:
            print(f"{i+1}/{len(rows)}; Failed to get length for {title}")
            cursor.execute("UPDATE articles SET length = 0 WHERE id = %s", (id,))

def get_edits_and_editors(cursor):
    cursor.execute("SELECT id, name FROM articles WHERE edits IS NULL OR editors IS NULL")

    for row in cursor.fetchall():
        id = row[0]
        title = row[1]
        results = query_wikipedia(title, "revisions")
        print(f"Getting edits and editors for {title}")

        edits = 0
        editors = set()
        anonymous = 0
        print(results)
        for k, v in results.items():
            if "revisions" not in v:
                for r in v["revisions"]:
                    edits += 1
                    if "user" in r:
                        editors.add(r["user"])
                    else:
                        anonymous += 1
                break
        
        cursor.execute("UPDATE articles SET edits = %s, editors = %s WHERE id = %s", (edits, len(editors) + anonymous, id))