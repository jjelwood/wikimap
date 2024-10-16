#this file retrieves the internal links of different article names
import requests

def get_links(cursor):
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php" # general api url link

    # for each article, based on its title, use the active session to fetch via the wikipedia api the internal links titles

    cursor.execute("SELECT id, name FROM articles")

    for row in cursor.fetchall():
        id = row[0]
        title = row[1]
        print("Internal links from the article\t"+title)
        PARAMS = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "links"
        }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()

        PAGES = DATA["query"]["pages"]

        for k, v in PAGES.items():
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

