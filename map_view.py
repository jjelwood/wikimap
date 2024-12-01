from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import sql

sql.cursor.execute("SELECT a.name, a.pageviews, p.latitude, p.longitude FROM articles a JOIN places p ON a.place_id = p.id WHERE p.latitude IS NOT NULL AND p.longitude IS NOT NULL and a.pageviews > 0")
rows = sql.cursor.fetchall()
data = pd.DataFrame(rows, columns=["name", "pageviews", "lat", "lon"])
fig = px.scatter_mapbox(
    data, 
    lat="lat", 
    lon="lon", 
    hover_name="name", 
    zoom=1,
    mapbox_style="open-street-map",
    size="pageviews",
    
)

map = html.Div([dcc.Graph(figure=fig)])