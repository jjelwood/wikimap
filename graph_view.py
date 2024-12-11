from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import sql
from Catergorical_Bubble_Plot_view import categorical_bubble_plot_view
from Bubble_Plot_Realibility_Population import bubble_plot_realibility_population_content
from podium import podium_content
import json
from podium import podium_content, update_podium_callback
from histogram import histogram_content


query = """
SELECT a.name, COALESCE(a.pageviews, 0), COALESCE(a.citations,0), COALESCE(COUNT(l.from_id),0) AS incoming_links, a.length 
FROM articles a
LEFT JOIN links l ON a.id = l.to_id
GROUP BY a.name, a.pageviews, a.citations, a.length
"""

sql.cursor.execute(query)
rows = sql.cursor.fetchall()
data = pd.DataFrame(rows, columns=["Name", "Pageviews", "Citations", "Incoming Links", "Article Length"])

filtered_data = data[
    (data["Incoming Links"] <= 200)
]

fig1 = px.scatter(filtered_data, x="Pageviews", y="Incoming Links", hover_name="Name", log_x=True, color="Article Length", color_continuous_scale="RdYlGn")
fig2 = px.scatter(data, x="Pageviews", y="Citations", hover_name="Name", log_x=True, color="Article Length", color_continuous_scale="RdYlGn")

content = html.Div([
    podium_content,
    html.Div(categorical_bubble_plot_view, id="categorical-bubble-plot"),
    histogram_content,
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    bubble_plot_realibility_population_content
], id="graph-content")
options = html.Div([
    html.P("This is an option in the graph view")
])
second_content = html.Div([
    html.P("This is the second content in the graph view")
])
callbacks = []