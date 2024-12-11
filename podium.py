from dash import html, dcc, Input, Output, State, ALL, ctx, callback_context
import sql
import json
from article_summary import get_article_summary
from country_summary import get_country_summary

# Dropdown options
dropdown_options = [
    {"label": "Viewed", "value": "Viewed"},
    {"label": "Cited", "value": "Cited"},
    {"label": "Linked To", "value": "Linked To"},
    {"label": "Linked From", "value": "Linked From"},
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
            SELECT articles.id, articles.name, articles.pageviews, places.country
            FROM articles
            JOIN places ON articles.place_id = places.id
            WHERE 1=1 {filter_query}
            ORDER BY articles.pageviews DESC
            LIMIT 3;
            """
        elif option == "Cited":
            query = f"""
            SELECT articles.id, articles.name, articles.citations, places.country
            FROM articles
            JOIN places ON articles.place_id = places.id
            WHERE 1=1 {filter_query}
            ORDER BY articles.citations DESC
            LIMIT 3;
            """
        elif option == "Linked To":
            query = f"""
            SELECT a.id, a.name, COUNT(l.from_id) AS links, places.country 
            FROM articles a
            JOIN places ON a.place_id = places.id
            JOIN links l ON a.id = l.to_id
            WHERE 1=1 {filter_query}
            GROUP BY a.name, places.country
            ORDER BY links DESC
            LIMIT 3;
            """
        elif option == "Linked From":
            query = f"""
            SELECT a.id, a.name, COUNT(l.to_id) AS links, places.country 
            FROM articles a
            JOIN places ON a.place_id = places.id
            JOIN links l ON a.id = l.from_id
            WHERE 1=1 {filter_query}
            GROUP BY a.name, places.country
            ORDER BY links DESC
            LIMIT 3;
            """
        elif option == "Reputable":
            query = f"""
            SELECT articles.id, articles.name, articles.reputability_score, places.country
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
        max_value = max(float(article[2]) for article in articles) or 1
        countries = [article[-1] for article in articles]

        # Generate podium content
        colors = ["#ffe08a", "#c7c7c7", "#f0c4a3"]
        medals = ["🥇", "🥈", "🥉"]
        podiums = []
        for i, article in enumerate(articles):
            value = float(article[2])
            height_percentage = (value / max_value) * 100  # Height proportional to the value
            podiums.append(
                html.Div([  # Each podium
                    html.Div(f"{medals[i]}", className="medal bg-primary"),
                    html.Img(src=f"assets/flags/{country_to_iso_code[countries[i]]}.svg", className="flag"),
                    html.Div(style={"height": f"{1.5 * height_percentage}px"}),  # Spacer
                    html.Div(article[1],
                             style={"text-align": "center", "font-weight": "bold", "margin-bottom": "10px"}),
                    html.Div(f"Value: {value:,}", style={"text-align": "center", "color": "gray"})
                ],
                id={"type": "podium-article", "index": article[0]},
                style={
                    "background-color": colors[i],
                    "cursor": "grab",
                }, className="podium-article")
            )
        
        # Rearrange the podiums
        podiums = [podiums[1], podiums[0], podiums[2]]

        return podiums
    
    @app.callback(
        Output("secondary-content", "children", allow_duplicate=True),
        [Input({"type": "podium-article", "index": ALL}, "n_clicks")],
        [State({"type": "podium-article", "index": ALL}, "id")],
        prevent_initial_call=True
    )
    def show_article_summary(n_clicks, ids):
        ctx = callback_context
        if not ctx.triggered or not any(n_clicks):
            return None
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        article_id = eval(button_id)["index"]
        print(article_id, n_clicks)
        return [get_article_summary(article_id)]