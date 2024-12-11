from dash import Dash, html, dcc, callback, Output, Input, State, callback_context
import plotly.express as px
import pandas as pd
import sql
import map_view
import graph_view
from podium import update_podium_callback

app = Dash(__name__, suppress_callback_exceptions=True)


def add_callback(output, inputs, func, prevent_initial_call=False):
    app.callback(output, inputs, prevent_initial_call, allow_duplicate=True)(func)


update_podium_callback(app)


def generate_content(button_id):
    if button_id == 'map-button':
        content = map_view.content
        options = map_view.options
        second_content = map_view.second_content
    elif button_id == 'graphs-button':
        content = graph_view.content
        options = graph_view.options
        second_content = graph_view.second_content

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

        html.Div([second_content], id="secondary-content"),

        content,
    ], id="section-content")


# Main callback to handle the page content
@app.callback(
    Output('page-content', 'children'),
    [Input('map-button', 'n_clicks'),
     Input('graphs-button', 'n_clicks')]
)
def display_page(map_clicks, graphs_click):
    if not callback_context.triggered:
        button_id = 'map-button'  # Default to 'map-button'
    else:
        button_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    return generate_content(button_id)


# Separate callback for updating the content of secondary-section (map or graph content)
@app.callback(
    Output('secondary-content', 'children'),
    [Input('map-button', 'n_clicks'),
     Input('graphs-button', 'n_clicks')]
)
def update_secondary_content(map_clicks, graphs_click):
    # Check which button was clicked using callback context
    if not callback_context.triggered:
        button_id = 'map-button'  # Default to 'map-button'
    else:
        button_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    # Return the appropriate second content based on the button clicked
    if button_id == 'map-button':
        return map_view.second_content
    elif button_id == 'graphs-button':
        return graph_view.second_content


# Separate callback to control the visibility of the options menu (hamburger)
@app.callback(
    [Output('options', 'style'), Output('options-menu', 'className')],
    [Input('hamburger', 'n_clicks')]
)
def toggle_options(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'block'}, ''
    else:
        return {'display': 'none'}, 'closed'


# Add all the callbacks from map_view and graph_view
for output, inputs, func, prevent_initial_call in map_view.callbacks:
    add_callback(output, inputs, func, prevent_initial_call)

for output, inputs, func, prevent_initial_call in graph_view.callbacks:
    add_callback(output, inputs, func, prevent_initial_call)

# App layout
app.layout = html.Div([
    # Title
    html.H1("Wikimap", id="title"),

    # Menu bar
    html.Div([
        html.Button("Map", id="map-button", n_clicks=0, className="menu-button"),
        html.Button("Graphs", id="graphs-button", n_clicks=0, className="menu-button"),
    ], id="menu"),

    # Main content
    html.Div(generate_content('map-button'), id='page-content'),
], id='root')

if __name__ == "__main__":
    app.run(debug=True)
