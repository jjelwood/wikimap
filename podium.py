from dash import html, dcc, Input, Output
import sql
import json

# Dropdown options
dropdown_options = [
    {"label": "Viewed", "value": "Viewed"},
    {"label": "Cited", "value": "Cited"},
    {"label": "Linked", "value": "Linked"},
    {"label": "Reputable", "value": "Reputable"}
]

continent_options = [
    {"label": "World", "value": "World"},
    {"label": "North America", "value": "North America"},
    {"label": "South America", "value": "South America"},
    {"label": "Africa", "value": "Africa"},
    {"label": "Europe", "value": "Europe"},
    {"label": "Asia", "value": "Asia"},
    {"label": "Oceania", "value": "Oceania"},
]

country_to_iso_code = json.load(open("iso_codes.json"))

# Layout for the podium
podium_content = html.Div([
    # Header with dropdowns
    html.Div([
        html.H2("Top 3 Most", className="podium-title"),
        dcc.Dropdown(
            id="category-dropdown",
            options=dropdown_options,
            value="Viewed",
            className="podium-dropdown",
        ),
        html.H2(" Articles In ", className="podium-title"),
        dcc.Dropdown(
            id="continent-dropdown",
            options=continent_options,
            value="World",
            className="podium-dropdown",
        ),
    ], id="podium-header"),

    # Podium container
    html.Div(id="podium", className="podium")
])


# Callback for updating the podium
def update_podium_callback(app):
    @app.callback(
        Output("podium", "children"),
        [Input("category-dropdown", "value"), Input("continent-dropdown", "value")]
    )
    def update_podium(option, continent):
        # Build query based on dropdown selections
        filter_query = ""
        if continent != "World":
            filter_query = f"AND places.continent = '{continent}'"

        if option == "Viewed":
            query = f"""
            SELECT articles.name, articles.pageviews, places.country
            FROM articles
            JOIN places ON articles.place_id = places.id
            WHERE 1=1 {filter_query}
            ORDER BY articles.pageviews DESC
            LIMIT 3;
            """
        elif option == "Cited":
            query = f"""
            SELECT articles.name, articles.citations, places.country
            FROM articles
            JOIN places ON articles.place_id = places.id
            WHERE 1=1 {filter_query}
            ORDER BY articles.citations DESC
            LIMIT 3;
            """
        elif option == "Linked":
            query = f"""
            SELECT a.name, COUNT(l.from_id) AS links, places.country 
            FROM articles a
            JOIN places ON a.place_id = places.id
            JOIN links l ON a.id = l.to_id
            WHERE 1=1 {filter_query}
            GROUP BY a.name, places.country
            ORDER BY links DESC
            LIMIT 3;
            """
        elif option == "Reputable":
            query = f"""
            SELECT articles.name, articles.reputability_score, places.country
            FROM articles
            JOIN places ON articles.place_id = places.id
            WHERE 1=1 {filter_query}
            ORDER BY articles.reputability_score DESC
            LIMIT 3;
            """
        else:
            return [html.Div("No articles found", style={"text-align": "center", "margin": "20px"})]

        sql.cursor.execute(query)
        articles = sql.cursor.fetchall()
        if not articles:
            return [html.Div("No articles found", style={"text-align": "center", "margin": "20px"})]

        # Get the maximum value for proportional height calculation
        max_value = max(article[1] for article in articles)
        countries = [article[-1] for article in articles]

        # Generate podium content
        colors = ["#ffe08a", "#c7c7c7", "#f0c4a3"]
        medals = ["🥇", "🥈", "🥉"]
        podiums = []
        for i, article in enumerate(articles):
            height_percentage = (article[1] / max_value) * 100  # Height proportional to the value
            print(height_percentage)
            podiums.append(
                html.Div([  # Each podium
                    html.Div(f"{medals[i]}", className="medal bg-primary"),
                    html.Img(src=f"assets/flags/{country_to_iso_code[countries[i]]}.svg", className="flag"),
                    html.Div(style={"height": f"{1.5 * height_percentage}px"}),  # Spacer
                    html.Div(article[0],
                             style={"text-align": "center", "font-weight": "bold", "margin-bottom": "10px"}),
                    html.Div(f"Value: {article[1]:,}", style={"text-align": "center", "color": "gray"})
                ], style={
                    "background-color": colors[i],
                }, className="podium-article")
            )
        
        # Rearrange the podiums
        podiums = [podiums[1], podiums[0], podiums[2]]

        return podiums