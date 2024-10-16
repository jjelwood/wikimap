import requests
import json


def get_pageviews(article, start_date, end_date):
    # Use 'monthly' instead of 'daily' in the URL to get monthly pageviews
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{article}/daily/{start_date}/{end_date}"

    headers = {
        'User-Agent': 'PageViewRetriever/1.0 (josejaviaa@gmail.com)'  # Replace with your email
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['items']  # Return only the 'items' list, which contains monthly views
    else:
        return response


def calculate_average_pageviews(pageviews_data):
    total_views = 0
    num_months = len(pageviews_data)

    for item in pageviews_data:
        total_views += item['views']

    # Calculate monthly average
    if num_months > 0:
        return total_views / num_months
    else:
        return 0


# Articles you want to track
articles = ["Cat", "Dog"]

# Specify the date range (format: YYYYMM)
# Get the past 6 months. For example, from 2023-04 to 2023-09
start_date = "20240401"  # Start date (YYYYMM01, first day of the month)
end_date = "20241030"  # End date (YYYYMMDD, last day of the month)

# Fetch data and calculate average for each article
for article in articles:
    pageviews_data = get_pageviews(article, start_date, end_date)
    if pageviews_data:
        average_views = calculate_average_pageviews(pageviews_data)
        print(f"Average monthly views for {article} (last 6 months): {average_views:.2f}")
    else:
        print(f"Error fetching data for {article}, response: {pageviews_data}")
