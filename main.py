from dash import Dash, html, dcc, callback, Output, Input, callback_context
import plotly.express as px
import pandas as pd
import sql
import map_view
import graph_view

app = Dash(__name__)

def generate_content(button_id):
    if button_id == 'map-button':
        content = map_view.content
        options = map_view.options
        second_content = map_view.second_content
    elif button_id == 'graphs-button':
        options = graph_view.options
        content = graph_view.content
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

        # Section Content
        html.Div([
            content,
            second_content,
        ], id="content-split"),
    ], id="section-content")

# Callbacks to update the content based on the URL
@app.callback(
    Output('page-content', 'children'),
    [Input('map-button', 'n_clicks'),
     Input('graphs-button', 'n_clicks')]
)
def display_page(map_clicks, graphs_click):
    if not callback_context.triggered:
        button_id = 'home-button'
    else:
        button_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    
    return generate_content(button_id)

@app.callback(
    [Output('options', 'style'), Output('options-menu', 'className')],
    [Input('hamburger', 'n_clicks')]
)
def toggle_options(n_clicks):
    if n_clicks % 2 == 0:
        return {'display': 'block'}, ''
    else:
        return {'display': 'none'}, 'closed'
    
for output, inputs, func in map_view.callbacks:
    app.callback(output, inputs)(func)

for output, inputs, func in graph_view.callbacks:
    app.callback(output, inputs)(func)

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
