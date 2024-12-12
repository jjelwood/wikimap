from dash import html

second_content = None
options = None
content = html.Div([
    html.H2("Welcome to Wikimap!"),
    html.P("Welcome to the Wikimap Wikipedia Explorer! This app allows you to explore the relationships between Wikipedia articles, their pageviews, and their reputability scores. You can navigate the app using the buttons above."),
    html.P("The app is divided into three main sections: the map, the graphs, and the home page. The map allows you to explore the relationships between articles geographically. The graphs section allows you to explore the relationships between pageviews, citations, and reputability scores. The home page provides a brief overview of the app."),
    html.P("To get started, click on the map button above to explore the map!"),
], id="home-content")