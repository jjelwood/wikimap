from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import sql

sql.cursor.execute("SELECT a.name, a.pageviews, p.latitude, p.longitude FROM articles a JOIN places p ON a.place_id = p.id WHERE p.latitude IS NOT NULL AND p.longitude IS NOT NULL and a.pageviews > 0")
rows = sql.cursor.fetchall()
data = pd.DataFrame(rows, columns=["name", "pageviews", "lat", "lon"])
fig = px.scatter_map(
    data, 
    lat="lat", 
    lon="lon", 
    hover_name="name", 
    zoom=1,
    size="pageviews",
)
fig.update_traces(
    cluster=dict(
        enabled=True,
    )
)
fig.update_layout(
    mapbox=dict(
        center=dict(lat=data["lat"].mean(), lon=data["lon"].mean()),
        zoom=3
    ),
    margin={"r":0,"t":0,"l":0,"b":0},
    mapbox_zoom=3,
    mapbox_center={"lat": data["lat"].mean(), "lon": data["lon"].mean()},
    uirevision='constant',
)

content = html.Div([
    dcc.Graph(figure=fig)
])
options = html.Div([
    html.P("This is an option in the map view")
])