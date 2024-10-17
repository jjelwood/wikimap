#this file retrieves the internal links of different article names
import requests

S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php" # general api url link

def query_wikipedia(title, prop):
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": prop
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
                continue
            for l in v["links"]:
                cursor.execute("SELECT id FROM articles WHERE name = %s", (l["title"],))
                result = cursor.fetchone()
                if result and result[0] != id:
                    print(id, title, result[0], l["title"])
                    cursor.execute(
                        "INSERT INTO links (from_id, from_name, to_id, to_name) VALUES (%s, %s, %s, %s)",
                        (id, title, result[0], l["title"])
                    )

def get_lengths(cursor):
    # for each article, based on its title, use the active session to fetch via the wikipedia api the length of the article

    cursor.execute("SELECT id, name FROM articles WHERE length IS NULL")

    for row in cursor.fetchall():
        id = row[0]
        title = row[1]
        results = query_wikipedia(title, "info")
        print(f"{title} is {results} characters long")

        for k, v in results.items():
            if "length" not in v:
                continue
            length = v["length"]
            cursor.execute("UPDATE articles SET length = %s WHERE id = %s", (length, id))

