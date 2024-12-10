def calculate_score(cursor):
    # Get the fields we need to calculate the reputability score
    query = """
        SELECT a.name, COALESCE(a.pageviews,0), COALESCE(a.citations,0), COALESCE(a.edits,0), COALESCE(a.editors,0), COALESCE(COUNT(l.from_id), 0) AS incoming_links
        FROM articles a
        LEFT JOIN links l ON a.id = l.to_id
        GROUP BY a.name, a.pageviews, a.citations, a.edits, a.editors
        """
    cursor.execute(query)
    rows = cursor.fetchall()

    # Extract the data for normalization
    pageviews = [row[1] for row in rows]
    citations = [row[2] for row in rows]
    edits = [row[3] for row in rows]
    editors = [row[4] for row in rows]
    incoming_links = [row[5] for row in rows]

    # Logarithmic scaling to reduce large disparities
    def log_scale(values):
        return [1 + (v if v > 0 else 0) for v in values]

    pageviews_scaled = log_scale(pageviews)
    citations_scaled = log_scale(citations)
    edits_scaled = log_scale(edits)
    editors_scaled = log_scale(editors)
    incoming_links_scaled = log_scale(incoming_links)

    # Get the maximum values for normalized fields
    max_pageviews = max(pageviews_scaled)
    max_citations = max(citations_scaled)
    max_edits = max(edits_scaled)
    max_editors = max(editors_scaled)
    max_incoming_links = max(incoming_links_scaled)

    # Assign weights to factors (adjust these weights as needed)
    weights = {
        "pageviews": 0.2,
        "citations": 0.3,
        "edits": 0.2,
        "editors": 0.1,
        "incoming_links": 0.2,
    }

    # Calculate the reputability score for each article
    for row in rows:
        name = row[0]
        pageviews_score = (log_scale([row[1]])[0] / max_pageviews) * weights["pageviews"]
        citations_score = (log_scale([row[2]])[0] / max_citations) * weights["citations"]
        edits_score = (log_scale([row[3]])[0] / max_edits) * weights["edits"]
        editors_score = (log_scale([row[4]])[0] / max_editors) * weights["editors"]
        incoming_links_score = (log_scale([row[5]])[0] / max_incoming_links) * weights["incoming_links"]

        # Weighted average
        reputability_score = pageviews_score + citations_score + edits_score + editors_score + incoming_links_score
        print(f"reputability score for {name} is {reputability_score}")
        # Update the database
        cursor.execute("UPDATE articles SET reputability_score = %s WHERE name = %s", (reputability_score, name))