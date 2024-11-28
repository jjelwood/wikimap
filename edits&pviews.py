import requests
import time
import traceback

# Function to get pageviews data
def get_pageviews(article, start_date, end_date):
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{article}/monthly/{start_date}/{end_date}"
    headers = {
        'User-Agent': 'PageViewRetriever/1.0 (youremail@example.com)'  # Replace with your email
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return 0, data['items']  # Return only the 'items' list, which contains monthly views
    else:
        time.sleep(3)
        return 1, f"Failed to make the request: {response}"

# Function to calculate average pageviews
def calculate_average_pageviews(pageviews_data):
    total_views = 0
    num_months = len(pageviews_data)
    for item in pageviews_data:
        total_views += item['views']
    if num_months > 0:
        return int(total_views / num_months)
    else:
        return 0

# Function to add pageviews to database
def add_pageviews(cursor):
    cursor.execute(f"SELECT name FROM articles WHERE pageviews IS NULL")
    rows = cursor.fetchall()
    start_date = "20240401"  # Start date (YYYYMM01, first day of the month)
    end_date = "20240930"  # End date (YYYYMMDD, last day of the month)
    for row in rows:
        time.sleep(1)
        article = row[0]
        try:
            status, pageviews_data = get_pageviews(article, start_date, end_date)
        except Exception as e:
            traceback.print_exc()
            print(f"Error with {article}!! Exception: {e}")
            time.sleep(3)
            continue
        if status == 0:
            average_views = calculate_average_pageviews(pageviews_data)
            query = f"UPDATE articles SET pageviews = %s WHERE name = %s"
            cursor.execute(query, (average_views, article))
            print(f"Average monthly views for {article} (last 6 months): {average_views}")
        else:
            print(f"Error fetching data for {article}, code = {status}, message: {pageviews_data}")

# Function to get edits data
def get_editsdata(article):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": article,
        "prop": "revisions",
        "rvprop": "timestamp|user",
        "rvlimit": "max"
    }
    headers = {
        'User-Agent': 'EditRetriever/1.0 (youremail@example.com)'  # Replace with your email
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        pages = data['query']['pages']
        edits = 0
        editors = set()
        for page_id, page_data in pages.items():
            if 'revisions' in page_data:
                edits += len(page_data['revisions'])
                for revision in page_data['revisions']:
                    editors.add(revision['user'])
        return 0, {"edits": edits, "editors": len(editors)}
    else:
        time.sleep(3)
        return 1, f"Failed to make the request: {response}"

# Function to add edits data to database
def add_editsdata(cursor):
    cursor.execute(f"SELECT name FROM articles WHERE edits IS NULL OR editors IS NULL")
    rows = cursor.fetchall()
    for row in rows:
        time.sleep(1)
        article = row[0]
        try:
            status, edit_info = get_editsdata(article)
        except Exception as e:
            traceback.print_exc()
            print(f"Error with {article}!! Exception: {e}")
            time.sleep(3)
            continue
        if status == 0:
            query = f"UPDATE articles SET edits = %s, editors = %s WHERE name = %s"
            cursor.execute(query, (edit_info["edits"], edit_info["editors"], article))
            print(f"Edits for {article}: {edit_info['edits']}, Editors: {edit_info['editors']}")
        else:
            print(f"Error fetching data for {article}, code = {status}, message: {edit_info}")

# Main function to combine everything
def main(cursor):
    add_pageviews(cursor)
    add_editsdata(cursor)
