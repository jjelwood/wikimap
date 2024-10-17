from bs4 import BeautifulSoup
import requests

def get_citations(cursor):
    cursor.execute("SELECT id, url, name FROM articles WHERE citations IS NULL")

    for row in cursor.fetchall():
        id = row[0]
        url = row[1]
        name = row[2]
        results = scrape_for_citations(url)
        print(f"{name} has {results} citations")
        cursor.execute("UPDATE articles SET citations = %s WHERE id = %s", (results, id))

def scrape_for_citations(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    references = soup.find_all('ol', class_='references')
    count = 0
    for ref in references:
        count += len(ref.find_all('li'))
    return count