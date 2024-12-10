from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import sql

# Query data
sql.cursor.execute("""SELECT 
        places.continent,
        YEAR(articles.date) AS year_of_birth,
        articles.pageviews,
        articles.name AS article_name
    FROM 
        articles
    INNER JOIN 
        places
    ON 
        articles.place_id = places.id
    WHERE 
        places.continent IS NOT NULL 
        AND articles.date IS NOT NULL 
        AND articles.place_id > 0;""")
rows = sql.cursor.fetchall()

# Create a DataFrame
data = pd.DataFrame(rows, columns=["continent", "year_of_birth", "page_views", "article_name"])

# Clean the data: Replace NaN in 'page_views' with 0 and ensure numeric type
data["page_views"] = pd.to_numeric(data["page_views"], errors="coerce").fillna(0)

# Generate the Plotly figure
fig = px.scatter(
    data,
    x="continent",
    y="year_of_birth",
    size="page_views",
    color="continent",
    hover_name="article_name",
    title="Bubble Plot of Wikipedia Articles by Continent and Year of Birth",
    labels={"continent": "Continent", "year_of_birth": "Year of Birth"},
    height=1500,  # Make the graph taller
    size_max=100  # Increase max size of bubbles
)

fig.update_layout(
    legend=dict(
        title="Continents",
        x=1.05,  # Move legend outside the plot
        y=1,
        traceorder="normal",
    ),
    yaxis=dict(
        tickmode="linear",
        tick0=0,
        dtick=100,  # Space y-axis ticks every 50 years
        range=[0, 2050],  # Set y-axis range
    ),
    xaxis=dict(
        tickangle=-45,  # Rotate x-axis labels
    )
)

# Dash layout for the bubble plot
bubble_plot_content = html.Div([
    dcc.Graph(figure=fig)
])
