from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import sql


# Aggregate Data by Country
query = """
SELECT 
    p.country AS country, 
    SUM(a.pageviews) AS total_pageviews, 
    AVG(a.reputability_score) AS avg_reputability,
    c.population
FROM articles a
INNER JOIN places p ON a.place_id = p.id
INNER JOIN countries c ON p.country = c.name
WHERE 
    p.continent IS NOT NULL 
    AND a.pageviews IS NOT NULL 
    AND a.place_id > 0
GROUP BY p.country
"""
sql.cursor.execute(query)
rows = sql.cursor.fetchall()

# Create a DataFrame for the aggregated data
data = pd.DataFrame(rows, columns=["country", "total_pageviews", "avg_reputability", "population"])
# Ensure all relevant columns are numeric
data["total_pageviews"] = pd.to_numeric(data["total_pageviews"], errors="coerce").fillna(0)
data["avg_reputability"] = pd.to_numeric(data["avg_reputability"], errors="coerce").fillna(0)
data["population"] = pd.to_numeric(data["population"], errors="coerce").fillna(0)

# Create the Bubble Plot
fig = px.scatter(
    data,
    x="population",
    y="avg_reputability",
    size="total_pageviews",  # Bubble size represents total page views
    text="country",  # Country names inside the bubbles
    color="country",  # Different colors for each country
    labels={
        "population": "Population (log scale)",
        "avg_reputability": "Reputability Score",
        "total_pageviews": "Total Page Views"
    },
    # width=2200,  # Increase graph width significantly
    # height=2000,  # Maintain a large height for clarity
    size_max=200  # Increase maximum bubble size further
)

# Customize Layout for Better Appearance
fig.update_traces(
    textposition='middle center',
    marker=dict(opacity=0.8, line=dict(width=1, color='DarkSlateGrey'))  # Add bubble borders and transparency
)
fig.update_layout(
    title=dict(
        text="Pageviews by Reputability and Population",
        font=dict(size=24, family="Arial Black"),
        x=0.5,
        xanchor="center"
    ),
    xaxis=dict(
        type="log",  # Logarithmic scale for better visualization of population
        title=dict(
            text="Population (log scale)",
            font=dict(size=18)
        ),
        tickangle=-45,  # Rotate x-axis labels for readability
        range=[4, 10]  # Ensure the range covers a wide population spread
    ),
    yaxis=dict(
        title=dict(
            text="Reputability Score",
            font=dict(size=18)
        ),
        range=[0, 0.5]  # Add some breathing space on the y-axis
    ),
    showlegend=False,  # Remove the legend for clarity
    margin=dict(l=50, r=50, t=100, b=50),  # Adjust margins for clarity
    autosize=True  # Prevent automatic resizing to maintain wider proportions
)

# Output the figure (integrate it into Dash)
bubble_plot_realibility_population_content = html.Div([
    dcc.Graph(figure=fig)
])