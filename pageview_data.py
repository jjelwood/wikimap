import requests
import time
import sql
import traceback

def get_pageviews(article, start_date, end_date):
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{article}/monthly/{start_date}/{end_date}"

    headers = {
        'User-Agent': 'PageViewRetriever/1.0 (josejaviaa@gmail.com)'  # Replace with your email
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return 0, data['items']  # Return only the 'items' list, which contains monthly views
    else:
        time.sleep(3)
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


# Articles you want to track
sql.cursor.execute(f"SELECT name FROM articles WHERE pageviews IS NULL")
rows = sql.cursor.fetchall()

# Specify the date range (format: YYYYMM)
# Get the past 6 months. For example, from 2023-04 to 2023-09
start_date = "20240401"  # Start date (YYYYMM01, first day of the month)
end_date = "20240930"  # End date (YYYYMMDD, last day of the month)

counter = 0
# Fetch data and calculate average for each article
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
        sql.cursor.execute(query, (average_views, article))
        print(f"Average monthly views for {article} (last 6 months): {average_views}")
        if counter == 20:
            counter = 0
            sql.conn.commit()
    else:
        print(f"Error fetching data for {article}, code = {status}, message: {pageviews_data}")
    counter += 1

sql.conn.commit()

# Close the connection
sql.cursor.close()
sql.conn.close()