from dash import Dash, html, dcc, callback, Output, Input, callback_context
import plotly.express as px
import pandas as pd
import sql
import map_view
import graph_view

app = Dash(__name__)

app.layout = html.Div([
    # Title
    html.H1("Wikimap"),

    # Menu bar
    html.Div([
        html.Button("Home", id="home-button", n_clicks=0, className="menu-button"),
        html.Button("Map", id="map-button", n_clicks=0, className="menu-button"),
        html.Button("Graphs", id="graphs-button", n_clicks=0, className="menu-button"),
    ], id="menu"),

    # Main content
    html.Div(id='page-content'),
], id='root')

# Callbacks to update the content based on the URL
@app.callback(
    Output('page-content', 'children'),
    [Input('home-button', 'n_clicks'),
     Input('map-button', 'n_clicks'),
     Input('graphs-button', 'n_clicks')]
)
def display_page(home_clicks, map_clicks, graphs_click):
    if not callback_context.triggered:
        button_id = 'home-button'
    else:
        button_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'map-button':
        options = map_view.options
        content = map_view.content
        second_content = map_view.second_content
    elif button_id == 'graphs-button':
        options = graph_view.options
        content = graph_view.content
        second_content = graph_view.second_content
    else:
        options = None
        content = html.H1("This is a test view")
        second_content = html.Div("This is second content goes")
        
    return html.Div([
        # Options Menu
        html.Div([
            # Hamburger menu icon
            html.Button("☰", id="hamburger", n_clicks=0),

            # Options Content
            html.Div([
                html.H2("Options"),
                options
            ], id="options"),
        ], id="options-menu"),

        # Section Content
        html.Div([
            content,
            second_content,
        ], id="content-split"),
    ], id="section-content")

@app.callback(
    Output('options', 'style'),
    [Input('hamburger', 'n_clicks')]
)
def toggle_options(n_clicks):
    if n_clicks % 2 == 0:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

if __name__ == "__main__":
    app.run(debug=True)
