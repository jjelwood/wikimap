import plotly.express as px
import pandas as pd
import sql
from dash import Dash, html, dcc

# Assuming your data query remains the same
sql.cursor.execute("SELECT a.id, a.name, a.pageviews, a.summary, p.latitude, p.longitude FROM articles a JOIN places p ON a.place_id = p.id WHERE p.latitude IS NOT NULL AND p.longitude IS NOT NULL and a.pageviews > 0")
rows = sql.cursor.fetchall()
data = pd.DataFrame(rows, columns=["id", "name", "pageviews", "summary", "lat", "lon"])

# Create a density heatmap for article concentration
fig = px.density_mapbox(
    data,
    lat="lat",
    lon="lon",
    radius=10,  # Adjust radius to control the size of the influence
    center=dict(lat=data["lat"].mean(), lon=data["lon"].mean()),
    zoom=3,
    mapbox_style="carto-positron",  # Choose the map style
    #color_continuous_scale="Jet",  # Change color scale (e.g., Viridis, Hot, Jet)
    range_color=(0, 40),  # Adjust the intensity range here
)

# Update layout for a cleaner display
fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    mapbox=dict(
        zoom=3,
        center={"lat": data["lat"].mean(), "lon": data["lon"].mean()},
    )
)

# Add the heatmap to your Dash app
view_heatmap_content = html.Div([
    dcc.Graph(figure=fig, id="heatmap")
])
