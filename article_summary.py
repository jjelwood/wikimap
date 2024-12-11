import sql
from dash import html

def get_summary(article_id):
    sql.cursor.execute("SELECT * FROM articles WHERE id = %s", (article_id,))
    article = sql.cursor.fetchone()
    if article is None:
        return {"display": "none"}, None
    id, name, date, place_id, summary, url, length, citations, edits, editors, pageviews, reputability_score = article
    info_content = html.Div([
        html.H4(f"Article Name: {name}"),
        html.P(f"Pageviews: {pageviews}"),
        html.P(f"Summary:{summary}")
    ])
    return {"display": "block"}, info_content