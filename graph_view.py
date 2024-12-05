from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import sql

query = """
SELECT a.name, log(a.pageviews), a.citations, COALESCE(COUNT(l.from_id),0) AS incoming_links 
FROM articles a
JOIN links l ON a.id = l.to_id
GROUP BY a.name, a.pageviews
"""

sql.cursor.execute(query)
rows = sql.cursor.fetchall()
data = pd.DataFrame(rows, columns=["Name", "Pageviews", "Citations", "Incoming Links"])
fig1 = px.scatter(data, x="pageviews", y="incoming_links", hover_name="name", log_x=True)
fig2 = px.scatter(data, x="pageviews", y="citations", hover_name="name", log_x=True)
graph = html.Div([dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)])