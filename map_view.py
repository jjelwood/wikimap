from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import sql
import article_summary
from heatmap import view_heatmap_content
import plotly.graph_objs as go
import json

sql.cursor.execute("SELECT a.id, a.name, a.pageviews, a.summary, p.latitude, p.longitude FROM articles a JOIN places p ON a.place_id = p.id WHERE p.latitude IS NOT NULL AND p.longitude IS NOT NULL and a.pageviews > 0")
rows = sql.cursor.fetchall()
data = pd.DataFrame(rows, columns=["id", "name", "pageviews","summary", "lat", "lon"])
fig = px.scatter_map(
    data, 
    lat="lat", 
    lon="lon", 
    hover_name="name", 
    zoom=1,
    size="pageviews",
    custom_data=["id", "name","pageviews","summary"]
)
fig.update_traces(
    cluster=dict(
        enabled=False,
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
    # Map
    dcc.Graph(figure=fig, id="map"),

    # Graph container for monthly pageviews (immediately below the map)
    html.Div(id="graph-container"),

    # Heatmap content can be added elsewhere if still needed
    view_heatmap_content
])
options = html.Div([
    dcc.Checklist(
        id='cluster-toggle',
        options=[{'label': 'Enable Clusters', 'value': 'enabled'}],
        value=[]
    ),
])
second_content = None

def update_map(cluster_toggle):
    if 'enabled' in cluster_toggle:
        fig.update_traces(cluster=dict(enabled=True,maxzoom=10,step=50))
    else:
        fig.update_traces(cluster=dict(enabled=False))
    return fig

# On_click event to show information related to articles
def on_click(click_data):
    if click_data is None:
        return None, None

    point = click_data["points"][0]
    custom_data = point.get("customdata")
    article_id = custom_data[0]

    # Query the monthly pageviews
    sql.cursor.execute("SELECT monthly_pageviews FROM articles WHERE id = %s", (article_id,))
    result = sql.cursor.fetchone()

    if not result or not result[0]:
        return None, None

    pageviews_dict = json.loads(result[0])  # Parse JSON string
    monthly_pageviews = list(pageviews_dict.values())
    months = [f"Month {i + 1}" for i in range(len(monthly_pageviews))]

    # Create the graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=monthly_pageviews, mode='lines+markers'))
    fig.update_layout(
        title="Monthly Pageviews",
        xaxis_title="Month",
        yaxis_title="Pageviews",
        margin={"l": 40, "r": 40, "t": 40, "b": 40}
    )

    # Return Dash components
    summary_component = article_summary.get_article_summary(article_id)

    return summary_component, dcc.Graph(figure=fig)

callbacks = [
    (
        Output('map', 'figure'),
        [Input('cluster-toggle', 'value')],
        update_map,
        False
    ),
    (
        [
            Output('secondary-content', 'children', allow_duplicate=True),
            Output('graph-container', 'children')
        ],
        [Input('map', 'clickData')],
        on_click,
        True
    )
]