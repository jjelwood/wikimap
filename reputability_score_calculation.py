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

    print(rows)

    # Get the maximum values for each field
    max_pageviews = max([row[1] for row in rows])
    max_citations = max([row[2] for row in rows])
    max_edits = max([row[3] for row in rows])
    max_editors = max([row[4] for row in rows])
    max_incoming_links = max([row[5] for row in rows])

    # Calculate the reputability score for each article
    for row in rows:
        name = row[0]
        pageviews = row[1]
        citations = row[2]
        edits = row[3]
        editors = row[4]
        incoming_links = row[5]

        pageviews_score = (pageviews / max_pageviews) if max_pageviews > 0 else 1
        citations_score = (citations / max_citations) if max_citations > 0 else 1
        edits_score = (edits / max_edits) if max_edits > 0 else 1
        editors_score = (editors / max_editors) if max_editors > 0 else 1
        incoming_links_score = (incoming_links / max_incoming_links) if max_incoming_links > 0 else 1

        reputability_score = (pageviews_score + citations_score + edits_score + editors_score + incoming_links_score) / 5

        cursor.execute("UPDATE articles SET reputability_score = %s WHERE name = %s", (reputability_score, name))