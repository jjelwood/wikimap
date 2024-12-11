from dash import html, dcc
import plotly.express as px
import pandas as pd
import sql

# Query data
sql.cursor.execute("""
    SELECT pageviews
    FROM articles
    WHERE pageviews IS NOT NULL;
""")
rows = sql.cursor.fetchall()

# Create a DataFrame
data = pd.DataFrame(rows, columns=["pageviews"])

# Clean the data: Ensure pageviews is numeric
data["pageviews"] = pd.to_numeric(data["pageviews"], errors="coerce").fillna(0)

# Generate the Plotly histogram
fig = px.histogram(
    data,
    x="pageviews",
   nbins=100,
   title="Distribution of Article Popularity",
   # labels={"pageviews": "Article Popularity"},
   #  log_x=True  # Use log scale for x-axis if needed
)
fig.update_layout(xaxis=dict(range=[0, 1_000_000]))
# Update layout for better appearance
# fig.update_layout(
#     title=dict(
#         text="Article Popularity Distribution",
#         font=dict(size=24, color="blue", family="Arial Black"),
#         x=0.5,
#         xanchor="center"
#     ),
#     xaxis=dict(
#         title=dict(
#             text="Article Popularity",
#             font=dict(size=18, color="darkblue", family="Arial"),
#         ),
#         type="log",  # Logarithmic scale for better visualization
#     ),
#     yaxis=dict(
#         title=dict(
#             text="Number of Articles",
#             font=dict(size=18, color="darkblue", family="Arial"),
#         ),
#     ),
#     bargap=0.1,  # Reduce gap between bars
# )

# Dash layout for the histogram
histogram_content = html.Div([
    dcc.Graph(figure=fig)
])
