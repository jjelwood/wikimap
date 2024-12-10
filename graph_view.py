from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import sql
from Catergorical_Bubble_Plot_view import categorical_bubble_plot_view
from Bubble_Plot_Realibility_Population import bubble_plot_realibility_population_content
import json

query = """
SELECT a.name, COALESCE(a.pageviews, 0), COALESCE(a.citations,0), COALESCE(COUNT(l.from_id),0) AS incoming_links 
FROM articles a
LEFT JOIN links l ON a.id = l.to_id
GROUP BY a.name, a.pageviews, a.citations
"""

sql.cursor.execute(query)
rows = sql.cursor.fetchall()
data = pd.DataFrame(rows, columns=["Name", "Pageviews", "Citations", "Incoming Links"])
fig1 = px.scatter(data, x="Pageviews", y="Incoming Links", hover_name="Name", log_x=True)
fig2 = px.scatter(data, x="Pageviews", y="Citations", hover_name="Name", log_x=True)

# User created views

categories = ["Viewed", "Cited", "Linked", "Young", "Reputable"]

podium = html.Div(id="podium-view", children=[
    html.Div([
        html.H2("Top 3 Most", className="podium-title", style={"display": "inline-block", "margin-right": "10px"}),
        dcc.Dropdown(
            id="category-dropdown",
            options=[{"label": category, "value": category} for category in categories],
            value="Viewed",
            style={"display": "inline-block", "width": "200px"}
        ),
        html.H2("Articles", className="podium-title", style={"display": "inline-block", "margin-left": "10px"})
    ], style={"display": "flex", "align-items": "center", "width": "100%"}),
    html.Div(id="podium", children=[
        # Silver
        html.Div(className="podium-article second-place", children=[
            html.Img(className="flag", src="assets/flags/ae.svg"),
            html.Div("🥈", className="medal"),
            html.Div("No articles found", className="article-list")
        ]),
        # Gold
        html.Div(className="podium-article first-place", children=[
            html.Img(className="flag"),
            html.Div("🥇", className="medal"),
            html.Div("No articles found", className="article-list")
        ]),
        # Bronze
        html.Div(className="podium-article third-place", children=[
            html.Img(className="flag"),
            html.Div("🥉", className="medal"),
            html.Div("No articles found", className="article-list")
        ])
    ])
])

flag_names = json.load(open("iso_codes.json"))

def update_podium(category):
    column = {
        "Viewed": "a.pageviews",
        "Cited": "a.citations",
        "Linked": "incoming_links",
        "Young": "a.date",
        "Reputable": "a.reputability_score"
    }[category]

    query = f"""
    SELECT 
        a.name,
        COALESCE(a.date, 0),
        COALESCE(a.pageviews, 0),
        COALESCE(a.citations,0),
        COALESCE(COUNT(l.from_id),0) AS incoming_links,
        a.reputability_score,
        p.name AS place_name
    FROM articles a
    LEFT JOIN links l ON a.id = l.to_id
    LEFT JOIN places p ON a.place_id = p.id
    GROUP BY a.name, a.pageviews, a.citations, a.date, a.reputability_score
    ORDER BY {column} DESC
    LIMIT 3
    """

    sql.cursor.execute(query)
    rows = sql.cursor.fetchall()
    data = pd.DataFrame(rows, columns=["Name", "Date", "Pageviews", "Citations", "Incoming Links", "Reputability Score", "Place Name"])
    data["flag"] = flag_names[data["Place Name"]]

    podium = []
    for i, row in data.iterrows():
        podium.append(
            html.Div(className="podium-article", children=[
                html.Img(className="flag", src=row["flag"]),
                html.Div(f"🥇🥈🥉"[i], className="medal"),
                html.Div(row["Name"], className="article-list")
            ])
        )

    podium = [podium[1], podium[0], podium[2]] # Reorder the podium

    return [
        html.Div(f"Selected category: {category}", className="podium-article")
    ]

# Exports

content = html.Div([
    podium,
    bubble_plot_content,
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    categorical_bubble_plot_view,
    bubble_plot_realibility_population_content
])
options = html.Div([
    html.P("This is an option in the graph view")
])
second_content = html.Div([
    html.P("This is the second content in the graph view")
])
callbacks = [(Output("podium", "children"),Input("category-dropdown", "value"), update_podium, False)]