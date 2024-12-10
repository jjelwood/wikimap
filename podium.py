from dash import html, dcc, Input, Output
import sql

# Dropdown options
dropdown_options = [
    {"label": "Viewed", "value": "Viewed"},
    {"label": "Cited", "value": "Cited"},
    {"label": "Linked", "value": "Linked"},
    {"label": "Reputable", "value": "Reputable"}
]

# Layout for the podium
podium_content = html.Div([
    # Header with dropdown in between
    html.Div([
        html.Span("Top 3 Most ", style={"font-size": "24px", "color": "blue"}),
        dcc.Dropdown(
            id="category-dropdown",
            options=dropdown_options,
            value="Viewed",
            style={"width": "150px", "display": "inline-block", "vertical-align": "middle"}
        ),
        html.Span(" Articles", style={"font-size": "24px", "color": "blue"}),
    ], style={"text-align": "center", "margin-bottom": "20px"}),

    # Podium container
    html.Div(id="podium", style={
        "display": "flex",
        "justify-content": "space-evenly",
        "align-items": "flex-end",  # Align podiums to the bottom
        "margin-top": "20px",
        "height": "300px",  # Fixed height for proportional scaling
    })
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

        # Get the maximum value for proportional height calculation
        max_value = max(article[1] for article in articles)

        # Generate podium content
        colors = ["gold", "silver", "brown"]
        podiums = []
        for i, article in enumerate(articles):
            height_percentage = (article[1] / max_value) * 100  # Height proportional to the value
            podiums.append(
                html.Div([  # Each podium
                    html.Div(f"{i + 1}", className="badge bg-primary",
                             style={"font-size": "20px", "margin-bottom": "10px"}),
                    html.Div(article[0],
                             style={"text-align": "center", "font-weight": "bold", "margin-bottom": "10px"}),
                    html.Div(f"Value: {article[1]}", style={"text-align": "center", "color": "gray"})
                ], style={
                    "background-color": colors[i],
                    "width": "30%",
                    "height": f"{height_percentage}%",  # Dynamic height
                    "padding": "10px",
                    "border-radius": "10px",
                    "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                    "text-align": "center",
                    "display": "flex",
                    "flex-direction": "column",
                    "justify-content": "flex-end",  # Align content to the bottom
                })
            )
        return podiums
