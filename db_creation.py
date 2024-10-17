import mysql.connector
import names_export
import wikidata_query
import wikipedia_query
import get_citations
import json
from sql import cursor

hard_reset = False

config = json.load(open('config.json'))

connection = mysql.connector.connect(
  host=config['sqlhost'],
  user=config['sqluser'],
  password=config['sqlpassword']
)

cursor = connection.cursor(buffered=True)

try:

    if hard_reset and input("Are you sure you want to delete the database? (y/n) ") == 'y':
        cursor.execute(f"DROP DATABASE IF EXISTS {config['sqldb']}")

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['sqldb']}")

    cursor.execute(f"USE {config['sqldb']}")

    cursor.execute("""CREATE TABLE IF NOT EXISTS `articles` (
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
        `pagerank` decimal(10,0) DEFAULT NULL,
        `reputability_score` decimal(10,0) DEFAULT NULL,
        PRIMARY KEY (`id`)
    );
    """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS `places` (
        `id` int NOT NULL,
        `name` varchar(255) DEFAULT NULL,
        `latitude` decimal(10,8) DEFAULT NULL,
        `longitude` decimal(11,8) DEFAULT NULL,
        PRIMARY KEY (`id`)
    );
    """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS `comments` (
        `id` int AUTO_INCREMENT,
        `article_id` int DEFAULT NULL,
        `article_name` varchar(255) DEFAULT NULL,
        `text` varchar(255) DEFAULT NULL,
        `date` datetime DEFAULT NULL,
        `username` varchar(255) DEFAULT NULL,
        PRIMARY KEY (`id`)
    );
    """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS `links` (
        `id` int NOT NULL AUTO_INCREMENT,
        `from_id` int DEFAULT NULL,
        `to_id` int DEFAULT NULL,
        `from_name` varchar(255) DEFAULT NULL,
        `to_name` varchar(255) DEFAULT NULL,
        PRIMARY KEY (`id`)
    );
    """)

    # names_export.export_names(cursor, 'C:\\Users\\jj\Downloads\\archive\\AgeDataset-V1.csv')
    # wikidata_query.add_places(cursor)
    # wikidata_query.populate_places(cursor)
    # wikipedia_query.get_links(cursor)
    # wikipedia_query.get_lengths(cursor)
    get_citations.get_citations(cursor)

finally:
    connection.commit()
    cursor.close()
    connection.close()
