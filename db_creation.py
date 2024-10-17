import names_export
import wikidata_query
import wikipedia_query
import get_citations
import json
import sql
import coordinate_finder
import pageview_data

hard_reset = False

config = json.load(open('config.json'))

try:
    if hard_reset and input("Are you sure you want to delete the database? (y/n) ") == 'y':
        sql.cursor.execute(f"DROP DATABASE IF EXISTS {config['sqldb']}")

    sql.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['sqldb']}")

    sql.cursor.execute(f"USE {config['sqldb']}")

    sql.cursor.execute("""CREATE TABLE IF NOT EXISTS `articles` (
        `id` int NOT NULL,
        `name` varchar(255) DEFAULT NULL,
        `place_id` int DEFAULT NULL,
        `summary` varchar(255) DEFAULT NULL,
        `url` varchar(255) DEFAULT NULL,
        `length` int DEFAULT NULL,
        `citations` int DEFAULT NULL,
        `edits` int DEFAULT NULL,
        `editors` int DEFAULT NULL,
        `created` datetime DEFAULT NULL,
        `pageviews` int DEFAULT NULL,
        `reputability_score` decimal(10,0) DEFAULT NULL,
        PRIMARY KEY (`id`)
    );
    """)

    sql.cursor.execute("""CREATE TABLE IF NOT EXISTS `places` (
        `id` int NOT NULL,
        `name` varchar(255) DEFAULT NULL,
        `latitude` decimal(10,8) DEFAULT NULL,
        `longitude` decimal(11,8) DEFAULT NULL,
        PRIMARY KEY (`id`)
    );
    """)

    # sql.cursor.execute("""CREATE TABLE IF NOT EXISTS `comments` (
    #     `id` int AUTO_INCREMENT,
    #     `article_id` int DEFAULT NULL,
    #     `article_name` varchar(255) DEFAULT NULL,
    #     `text` varchar(255) DEFAULT NULL,
    #     `date` datetime DEFAULT NULL,
    #     `username` varchar(255) DEFAULT NULL,
    #     PRIMARY KEY (`id`)
    # );
    # """)

    sql.cursor.execute("""CREATE TABLE IF NOT EXISTS `links` (
        `id` int NOT NULL AUTO_INCREMENT,
        `from_id` int DEFAULT NULL,
        `to_id` int DEFAULT NULL,
        `from_name` varchar(255) DEFAULT NULL,
        `to_name` varchar(255) DEFAULT NULL,
        PRIMARY KEY (`id`)
    );
    """)

    # names_export.export_names(sql.cursor, config['names_path'])
    # wikidata_query.add_places(sql.cursor)
    # wikidata_query.populate_places(sql.cursor)
    # wikipedia_query.get_links(sql.cursor)
    # wikipedia_query.get_lengths(sql.cursor)
    get_citations.get_citations(sql.cursor)
    coordinate_finder.add_coordinates(sql.cursor)
    pageview_data.add_pageviews(sql.cursor)

finally:
    sql.conn.commit()
    sql.cursor.close()
    sql.conn.close()
