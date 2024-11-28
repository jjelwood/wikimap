from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import sql

query = """
SELECT a.name, a.pageviews, COUNT(l.from_id) AS incoming_links 
FROM articles a
JOIN links l ON a.id = l.to_id
GROUP BY a.name, a.pageviews
"""

sql.cursor.execute(query)
rows = sql.cursor.fetchall()
data = pd.DataFrame(rows, columns=["name", "pageviews", "incoming_links"])
fig = px.scatter(data, x="pageviews", y="incoming_links", hover_name="name")
graph = html.Div([dcc.Graph(figure=fig)])