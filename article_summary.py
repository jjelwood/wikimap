import sql
from dash import html
import dash_cytoscape as cyto
def generate_graph_elements(article_name, linked_articles):

    elements = []

    # Add the central article node
    elements.append({"data": {"id": article_name, "label": article_name}, "classes": "central"})

    # Add nodes and edges for linked articles
    for row in linked_articles:
        to_name = row[0]
        elements.append({"data": {"id": to_name, "label": to_name}})
        elements.append({"data": {"source": article_name, "target": to_name}})
    
    cytoscape_graph = cyto.Cytoscape(
        id='cytoscape-graph',
        elements=elements,
        style={'width': '100%', 'height': '150px', 'margin-top': '10px'},
        layout={'name': 'circle', 'avoidOverlap': True, 'padding': 10},
        stylesheet=[
            {
                "selector": "node",
                "style": {
                    "content": "data(label)",
                    "text-halign": "center",
                    "text-valign": "center",
                    "background-color": "#1E90FF",  # A lighter blue
                    # "color": "white",
                    "font-size": "10px",
                    "text-valign": "top",  # Move text above the node
                    "text-margin-y": -5,  # Add a margin above the node
                    "border-width": 2,
                    "border-color": "#0074D9",
                    "width": 20,
                    "height": 20
                }
            },
            {
                "selector": "edge",
                "style": {
                    "width": 1.5,
                    "line-color": "#A9A9A9",  # Light gray to reduce visual noise
                    "target-arrow-color": "#A9A9A9",
                    "target-arrow-shape": "triangle",
                    "arrow-scale": 1.2,
                    "curve-style": "straight"  # Simpler and less distracting
                }
            },
            {
                "selector": ".central",
                "style": {
                    "background-color": "#FF851B",  # Orange to match reputability score styling
                    "font-size": "12px",
                    "width": 25,
                    "height": 25,
                    "border-width": 3,
                    "border-color": "#FF4136"  # Red border for emphasis
                }
            }
        ]
    )
    return cytoscape_graph
def get_article_summary(article_id):
    sql.cursor.execute("""
        SELECT a.id, a.name, a.date, p.name, a.summary, a.url, a.length, a.citations, a.pageviews, a.reputability_score, p.country 
        FROM articles a
        JOIN places p ON a.place_id = p.id
        WHERE a.id = %s
    """, (article_id,))
    article = sql.cursor.fetchone()
    id, name, date, place, summary, url, length, citations, pageviews, reputability_score, country = article
    if article is None:
        return None
    sql.cursor.execute("""
        SELECT to_name FROM links WHERE from_name = %s""",(name,))
    linked_articles = sql.cursor.fetchall()
    if linked_articles:
        cyto_graph=generate_graph_elements(name,linked_articles)
        cyto_graph_div=html.Div(cyto_graph,style={"margin-top":"20px"})
    else:
        cyto_graph_div = html.Div("No links found",
                            style={
        "text-align": "center",
            "margin-top": "20px",
            "color": "gray",
        "font-size": "16px",
            "font-style": "italic"
        })
        
    # Create styled component
    info_content = html.Div([
        # Header with title and reputability score badge
        html.Div([
            html.H4(name, className="article-title"),
            html.Span(f"✦ {reputability_score}", className="reputation-badge"),
        ], className="header-container"),

        # Summary section
        html.P(summary.capitalize(), className="article-summary"),

        # Key metrics section
        html.Div([
            html.Div([
                html.Span("📅", className="icon"),
                html.P(f"Date of Birth: {date.date() if date else 'No date found'}", className="metric-text"),
            ], className="metric"),
            html.Div([
                html.Span("👁️", className="icon"),
                html.P(f"Average Monthly Pageviews: {pageviews:,}", className="metric-text"),
            ], className="metric"),
            html.Div([
                html.Span("📚", className="icon"),
                html.P(f"Citations: {citations:,}", className="metric-text"),
            ], className="metric"),
            html.Div([
                html.Span("📏", className="icon"),
                html.P(f"Length: {length:,} words", className="metric-text"),
            ], className="metric"),
            html.Div([
                html.Span("📍", className="icon"),
                html.P(f"Birthplace: {place}", className="metric-text"),
            ], className="metric"),
            html.Div([
                html.Span("🌍", className="icon"),
                html.P(f"Birth Country: {country}", className="metric-text"),
            ], className="metric"),
        ], className="metrics-grid"),

        cyto_graph_div,
        # Footer with a "Read More" button
        html.Div([
            html.A("Read More", href=url, target="_blank", className="read-more-button"),
        ], className="footer-container"),
    ], className="article-summary-container")

    return info_content