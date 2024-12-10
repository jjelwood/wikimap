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
title=dict(
        text="Bubble Plot of Wikipedia Articles by Continent and Year of Birth",
        font=dict(size=24, color="black", family="Arial Black"),  # Bigger, bold title
        x=0.5,  # Center the title
        xanchor="center"
    ),
    legend=dict(
        title=dict(
            text="Continents",
            font=dict(size=16, color="darkblue", family="Arial Black")  # Bold legend title
        ),
        font=dict(size=14, color="black", family="Arial"),  # Legend item font styling
        bgcolor="rgba(255, 255, 255, 0.9)",  # Semi-transparent white background for better contrast
        bordercolor="black",  # Add a border around the legend
        borderwidth=2,  # Set border width
        x=1.05,  # Move legend outside the plot
        y=1,
        xanchor="left",
        yanchor="top",
    ),
    yaxis=dict(
        title=dict(
            text="Year of Birth",
            font=dict(size=18, color="darkblue", family="Arial"),  # Bold and larger font for y-axis label
        ),
        tickmode="linear",
        tick0=0,
        dtick=50,  # Space y-axis ticks every 50 years
        range=[0, 2050],  # Set y-axis range
    ),
    xaxis=dict(
        title=dict(
            text="Continent",
            font=dict(size=18, color="darkblue", family="Arial"),  # Bold and larger font for x-axis label
        ),
        tickangle=-45,  # Rotate x-axis labels
    ),  # Rotate x-axis labels
)

# Dash layout for the bubble plot
categorical_bubble_plot_view = html.Div([
    dcc.Graph(figure=fig)
])
