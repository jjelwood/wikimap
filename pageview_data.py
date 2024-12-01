import requests
import time
import traceback

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
    # Articles you want to track
    cursor.execute(f"SELECT name FROM articles WHERE pageviews IS NULL")
    rows = cursor.fetchall()

    # Specify the date range (format: YYYYMM)
    # Get the past 18 months. For example, from 2023-04 to 2024-09
    start_date = "20230401"  # Start date (YYYYMM01, first day of the month)
    end_date = "20240930"  # End date (YYYYMMDD, last day of the month)

    # Fetch data and calculate average for each article
    for row in rows:
        article = row[0]
        try:
            status, pageviews_data = get_pageviews(article, start_date, end_date)
        except Exception as e:
            traceback.print_exc()
            print(f"Error with {article}!! Exception: {e}")
            continue
        if status == 0:
            average_views = calculate_average_pageviews(pageviews_data)
            query = f"UPDATE articles SET pageviews = %s WHERE name = %s"
            cursor.execute(query, (average_views, article))
            print(f"Average monthly views for {article} (last 18 months): {average_views}")
        else:

            print(f"Error fetching data for {article}, code = {status}, message: {pageviews_data}")
