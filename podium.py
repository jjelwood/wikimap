from dash import html, dcc, Input, Output
import sql

# Dropdown options
dropdown_options = [
    {"label": "Viewed", "value": "Viewed"},
    {"label": "Cited", "value": "Cited"},
    {"label": "Linked", "value": "Linked"},
    {"label": "Young", "value": "Young"},
    {"label": "Reputable", "value": "Reputable"}
]

# Layout for the podium
podium_content = html.Div([
    html.H2("Top 3 Most Articles", style={"text-align": "center", "color": "blue"}),
    dcc.Dropdown(
        id="category-dropdown",
        options=dropdown_options,
        value="Viewed",
        style={"width": "50%", "margin": "auto"}
    ),
    html.Div(id="podium", style={"display": "flex", "justify-content": "space-evenly", "margin-top": "20px"})
])


# Callback for updating the podium
def update_podium_callback(app):
    @app.callback(
        Output("podium", "children"),
        [Input("category-dropdown", "value")]
    )
    def update_podium(option):
        print(f"Dropdown option selected: {option}")  # Debug
        # Query based on dropdown selection
        query = ""
        if option == "Viewed":
            query = """
            SELECT name, pageviews
            FROM articles
            ORDER BY pageviews DESC
            LIMIT 3;
            """
        elif option == "Cited":
            query = """
            SELECT name, citations
            FROM articles
            ORDER BY citations DESC
            LIMIT 3;
            """
        elif option == "Linked":
            query = """
            SELECT a.name, COUNT(l.from_id) AS links
            FROM articles a
            JOIN links l ON a.id = l.to_id
            GROUP BY a.name
            ORDER BY links DESC
            LIMIT 3;
            """
        elif option == "Young":
            query = """
            SELECT name, created
            FROM articles
            ORDER BY created DESC
            LIMIT 3;
            """
        elif option == "Reputable":
            query = """
            SELECT name, reputability_score
            FROM articles
            ORDER BY reputability_score DESC
            LIMIT 3;
            """
        sql.cursor.execute(query)
        articles = sql.cursor.fetchall()
        print(f"Articles retrieved: {articles}")  # Debug
        # No articles found case
        if not articles:
            return [html.Div("No articles found", style={"text-align": "center", "margin": "20px"})]

        # Generate podium content
        colors = ["gold", "silver", "bronze"]
        podiums = []
        for i, article in enumerate(articles):
            podiums.append(
                html.Div([
                    html.Div(f"{i + 1}", className="badge bg-primary",
                             style={"font-size": "20px", "margin-bottom": "10px"}),
                    html.Div(article[0],
                             style={"text-align": "center", "font-weight": "bold", "margin-bottom": "10px"}),
                    html.Div(f"Value: {article[1]}", style={"text-align": "center", "color": "gray"})
                ], style={
                    "background-color": colors[i],
                    "width": "30%",
                    "padding": "10px",
                    "border-radius": "10px",
                    "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                    "text-align": "center"
                })
            )
        return podiums
