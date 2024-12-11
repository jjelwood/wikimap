import requests
import time
import traceback
import json
import sql

def get_pageviews(article, start_date, end_date, language="en"):
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{language}.wikipedia/all-access/user/{article}/monthly/{start_date}/{end_date}"

    headers = {
        'User-Agent': 'PageViewRetriever/1.0 (jjelwood2005@gmail.com)'  # Replace with your email
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return 0, data['items']  # Return only the 'items' list, which contains monthly views
    else:
        print(f"Failed to make the request: {response.text}")
        return 1, f"Failed to make the request: {response}"


def calculate_average_pageviews(pageviews_data):
    total_views = 0
    num_months = len(pageviews_data)
    for item in pageviews_data:
        total_views += item['views']

    # Calculate monthly average
    if num_months > 0:
        return int(total_views / num_months)
    else:
        return 0

def add_pageviews(cursor):
    # Check if the 'monthly_pageviews' column exists, and add it if it doesn't
    cursor.execute("SHOW COLUMNS FROM articles LIKE 'monthly_pageviews'")
    result = cursor.fetchone()
    if not result:
        print("Adding 'monthly_pageviews' column to the 'articles' table...")
        cursor.execute("ALTER TABLE articles ADD COLUMN monthly_pageviews TEXT")

    # Fetch the articles to track
    cursor.execute(f"SELECT name FROM articles WHERE monthly_pageviews IS NULL AND pageviews IS NOT NULL")
    rows = cursor.fetchall()

    # Specify the date range (format: YYYYMM)
    start_date = "20220901"  # Start date (YYYYMM01, first day of the month)
    end_date = "20240930"  # End date (YYYYMMDD, last day of the month)

    # Fetch data and calculate average for each article
    counter = 0
    for row in rows:
        counter += 1
        if counter == 1000:
            counter = 0
            sql.conn.commit()

        article = row[0]
        try:
            # Replace this with the actual method to fetch pageviews
            status, pageviews_data = get_pageviews(article, start_date, end_date)
        except Exception as e:
            traceback.print_exc()
            print(f"Error with getting pageview data for {article}!! Exception: {e}")
            continue

        if status == 0:
            average_views = calculate_average_pageviews(pageviews_data)
            # Extract monthly pageviews into a dictionary
            monthly_data = {item["timestamp"]: item["views"] for item in pageviews_data}
            monthly_data_json = json.dumps(monthly_data)  # Convert to JSON string

            # Update the database with average and monthly pageviews
            query = f"UPDATE articles SET pageviews = %s, monthly_pageviews = %s WHERE name = %s"
            cursor.execute(query, (average_views, monthly_data_json, article))
            print(f"Updated {article} with average views and monthly data")
        else:
            print(f"Error fetching data for {article}, code = {status}, message: {pageviews_data}")
