import names_export
import wikidata_query
import wikipedia_query
import get_citations
import json
import sql
import coordinate_finder
import pageview_data
import get_reddit_data
import reputability_score_calculation
import add_country_data

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
        `date` datetime DEFAULT NULL,
        `place_id` int DEFAULT NULL,
        `summary` varchar(255) DEFAULT NULL,
        `url` varchar(255) DEFAULT NULL,
        `length` int DEFAULT NULL,
        `citations` int DEFAULT NULL,
        `edits` int DEFAULT NULL,
        `editors` int DEFAULT NULL,
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

    sql.cursor.execute("""CREATE TABLE IF NOT EXISTS `posts` (
        `id` int AUTO_INCREMENT,
        `name` varchar(255),
        `submission_id` varchar(255) DEFAULT NULL,
        `submission_title` varchar(1000) DEFAULT NULL,
        `submission_url` varchar(1000) DEFAULT NULL,          
        `submission_score` int DEFAULT NULL,
        `submission_author` varchar(255) DEFAULT NULL,
        PRIMARY KEY (`id`)
    );
    """)

    sql.cursor.execute("""CREATE TABLE IF NOT EXISTS `links` (
        `id` int NOT NULL AUTO_INCREMENT,
        `from_id` int DEFAULT NULL,
        `to_id` int DEFAULT NULL,
        `from_name` varchar(255) DEFAULT NULL,
        `to_name` varchar(255) DEFAULT NULL,
        PRIMARY KEY (`id`)
    );
    """)

    chunk_size = 10_000
    articles = 10_000
    #names = names_export.NameGenerator(config['names_path'])
    #names_export.update_urls(sql.cursor)
    try:
        for i in range(0, articles + 1, chunk_size):
            try:
                # names_export.export_names(sql.cursor, chunk_size, names)
                # wikidata_query.add_places_summaries_and_birthdates(sql.cursor)
                # wikidata_query.populate_places(sql.cursor)
                # wikipedia_query.get_lengths(sql.cursor)
                # wikipedia_query.get_edits_and_editors(sql.cursor)
                # get_citations.get_citations(sql.cursor)
                # coordinate_finder.add_coordinates(sql.cursor)
                # pageview_data.add_pageviews(sql.cursor)
                # get_reddit_data.get_reddit_data(sql.cursor)
                pass
            except Exception as e:
                print("Error:", e)
            finally:
                print("Processed articles up to", i)
                sql.conn.commit()
    except Exception as e:
        print("Error:", e)
    finally: # These operations have to be done over the entire dataset, so they are not chunked
        # wikipedia_query.get_links(sql.cursor)
        # reputability_score_calculation.calculate_score(sql.cursor)
        # add_country_data.add_country_and_continent_to_places(sql.cursor)
        # add_country_data.add_country_data(sql.cursor)
        pass
except Exception as e:
    print(e)
finally:
    print("Committing changes...")
    sql.conn.commit()
    sql.cursor.close()
    sql.conn.close()
