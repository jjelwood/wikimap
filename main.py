from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import sql
import map_view
import graph_view

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Wikipedia Dashboard"),
    map_view.map,
    graph_view.graph,
])

if __name__ == "__main__":
    app.run(debug=True)
