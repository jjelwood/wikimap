import sql
from dash import html

def get_article_summary(article_id):
    sql.cursor.execute("""
        SELECT a.id, a.name, a.date, p.name, a.summary, a.url, a.length, a.citations, a.pageviews, a.reputability_score, p.country 
        FROM articles a
        JOIN places p ON a.place_id = p.id
        WHERE a.id = %s
    """, (article_id,))
    article = sql.cursor.fetchone()
    id, name, date, place, summary, url, length, citations, pageviews, reputability_score, country = article
    if article is None:
        return None

    # Create styled component
    info_content = html.Div([
        # Header with title and reputability score badge
        html.Div([
            html.H4(name, className="article-title"),
            html.Span(f"✦ {reputability_score}", className="reputation-badge"),
        ], className="header-container"),

        # Summary section
        html.P(summary.capitalize(), className="article-summary"),

        # Key metrics section
        html.Div([
            html.Div([
                html.Span("📅", className="icon"),
                html.P(f"Date of Birth: {date.date() if date else 'No date found'}", className="metric-text"),
            ], className="metric"),
            html.Div([
                html.Span("👁️", className="icon"),
                html.P(f"Average Monthly Pageviews: {pageviews:,}", className="metric-text"),
            ], className="metric"),
            html.Div([
                html.Span("📚", className="icon"),
                html.P(f"Citations: {citations:,}", className="metric-text"),
            ], className="metric"),
            html.Div([
                html.Span("📏", className="icon"),
                html.P(f"Length: {length:,} words", className="metric-text"),
            ], className="metric"),
            html.Div([
                html.Span("📍", className="icon"),
                html.P(f"Birthplace: {place}", className="metric-text"),
            ], className="metric"),
            html.Div([
                html.Span("🌍", className="icon"),
                html.P(f"Birth Country: {country}", className="metric-text"),
            ], className="metric"),
        ], className="metrics-grid"),

        # Footer with a "Read More" button
        html.Div([
            html.A("Read More", href=url, target="_blank", className="read-more-button"),
        ], className="footer-container"),
    ], className="article-summary-container")

    return info_content