from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import sql

sql.cursor.execute("SELECT a.name, p.latitude, p.longitude FROM articles a JOIN places p ON a.place_id = p.id WHERE p.latitude IS NOT NULL AND p.longitude IS NOT NULL")
rows = sql.cursor.fetchall()
data = pd.DataFrame(rows, columns=["name", "lat", "lon"])
fig = px.scatter_mapbox(data, lat="lat", lon="lon", hover_name="name", zoom=1)
fig.update_layout(mapbox_style="open-street-map")
map = html.Div([dcc.Graph(figure=fig)])