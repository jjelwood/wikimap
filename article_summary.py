import sql
from dash import html

def get_article_summary(article_id):
    sql.cursor.execute("SELECT * FROM articles WHERE id = %s", (article_id,))
    article = sql.cursor.fetchone()
    if article is None:
        return None
        return {"display": "none"}, None

    info_content = html.Div([
        html.H4(f"Article Name: {name}"),
        html.P(f"Pageviews: {pageviews}"),
        html.P(f"Summary:{summary}")
    ])
    return info_content