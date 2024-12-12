from dash import Dash, html, dcc, callback_context, Output, Input
import plotly.express as px
import pandas as pd
import sql
import json
from Catergorical_Bubble_Plot_view import categorical_bubble_plot_view
from Bubble_Plot_Realibility_Population import bubble_plot_realibility_population_content
from podium import podium_content
from article_summary import get_article_summary
from country_summary import get_country_summary


query = """
SELECT a.id, a.name, COALESCE(a.pageviews, 0), COALESCE(a.citations,0), COALESCE(COUNT(l.from_id),0) AS incoming_links 
FROM articles a
LEFT JOIN links l ON a.id = l.to_id
GROUP BY a.id, a.name, a.pageviews, a.citations
"""

sql.cursor.execute(query)
rows = sql.cursor.fetchall()
data = pd.DataFrame(rows, columns=["Id", "Name", "Pageviews", "Citations", "Incoming Links"])
fig1 = px.scatter(data, x="Pageviews", y="Incoming Links", hover_name="Name", log_x=True, custom_data=["Id"])
fig2 = px.scatter(data, x="Pageviews", y="Citations", hover_name="Name", log_x=True, custom_data=["Id"])

country_name_to_iso_code = json.load(open("iso_codes.json"))

content = html.Div([
    html.Div([
        podium_content,
        html.P("See the top 3 articles across different metrics, try it out!")
    ], className="caption-container"),
    html.Div([
        categorical_bubble_plot_view,
        html.P("See what most popular articles are from each century from each continent! In this plot, the size of a bubble represents the average number of pageviews an article gets a month, and the color represents the continent the article is from.")
    ], className="caption-container", id="categorical-bubble-plot-container"),
    html.Div([
        dcc.Graph(figure=fig1, id="scatter-plot1"),
        html.P("See the relationship between pageviews and incoming links.")
    ], className="caption-container"),
    html.Div([
        dcc.Graph(figure=fig2, id="scatter-plot2"),
        html.P("See the relationship between the average number of pageviews an article gets and the number of citations it has.")
    ], className="caption-container"),
    html.Div([
        bubble_plot_realibility_population_content,
        html.P("Do countries with higher populations have articles with higher reputability scores? In this plot the size of a bubble represents the total number of pageviews articles in a country get a month, the color represents the country, and the x-axis represents the population of the country.")
    ], className="caption-container", id="bubble-plot-container")
], id="graph-content")
options = None
second_content = None

def show_article_summary(data1, data2, data3):
    # Find the id of the callback that was triggered
    if callback_context.triggered_id == "scatter-plot1":
        data = data1
    elif callback_context.triggered_id == "scatter-plot2":
        data = data2
    elif callback_context.triggered_id == "bubble-plot1":
        data = data3
    id = data["points"][0]["customdata"][0]
    return {"display": "block"}, [get_article_summary(id)]

def show_country_summary(data):
    if data is None:
        return {"display": "none"}, None
    name = data["points"][0]["customdata"][0]
    return {"display": "block"}, [get_country_summary(name)]

callbacks = [
    (
        [
            Output("secondary-content-container", "style", allow_duplicate = True),
            Output("secondary-content", "children", allow_duplicate = True)
        ],
        [
            Input("scatter-plot1", "clickData"), 
            Input("scatter-plot2", "clickData"),
            Input("bubble-plot1", "clickData")
        ],
        show_article_summary,
        True
    ),
    (
        [
            Output("secondary-content-container", "style", allow_duplicate = True),
            Output("secondary-content", "children", allow_duplicate = True),
        ],
        [Input("bubble-plot2", "clickData")],
        show_country_summary,
        True
    )
]