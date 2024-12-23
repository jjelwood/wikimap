import sql
from dash import html
import json

country_name_to_iso_code = json.load(open("iso_codes.json"))

def get_country_summary(country_name):
    sql.cursor.execute("""
    SELECT 
        p.country AS country, 
        SUM(a.pageviews) AS total_pageviews, 
        AVG(a.reputability_score) AS avg_reputability,
        c.population,
        COUNT(a.id) AS article_count
    FROM articles a
    INNER JOIN places p ON a.place_id = p.id
    INNER JOIN countries c ON p.country = c.name
    WHERE 
        p.continent IS NOT NULL 
        AND a.pageviews IS NOT NULL 
        AND a.place_id > 0
        AND p.country = %s
    GROUP BY p.country
    """, (country_name,))
    data = sql.cursor.fetchone()
    if data is None:
        return None
    
    name, total_pageviews, avg_reputability, population, article_count = data
    iso_code = country_name_to_iso_code.get(name, "unknown")

    return html.Div([
        # Country Header with Flag
        html.Div([
            html.H2(name, className="country-title"),
            html.Img(
                src=f"assets/flags/{iso_code}.svg", 
                alt=f"Flag of {name}", 
                className="country-flag"
            ),
        ], className="country-header"),
        
        # Statistics section
        html.Div([
            html.Div([
                html.Span("👁️", className="icon"),
                html.P(f"Total Pageviews: {total_pageviews:,}", className="metric-text"),
            ], className="metric"),
            html.Div([
                html.Span("📊", className="icon"),
                html.P(f"Average Reputability: {avg_reputability:.2f}", className="metric-text"),
            ], className="metric"),
            html.Div([
                html.Span("👥", className="icon"),
                html.P(f"Population: {population:,}", className="metric-text"),
            ], className="metric"),
            html.Div([
                html.Span("📰", className="icon"),
                html.P(f"Number of Articles: {article_count:,}", className="metric-text"),
            ], className="metric"),
        ], className="metrics"),
    ], className="country-summary-container")
