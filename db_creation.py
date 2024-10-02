import mysql.connector
import names_export

hard_reset = True

connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password"
)

cursor = connection.cursor(buffered=True)

try:
    if hard_reset:
        cursor.execute("DROP DATABASE IF EXISTS wikimap")

    cursor.execute("CREATE DATABASE IF NOT EXISTS wikimap")

    cursor.execute("USE wikimap")

    cursor.execute("""CREATE TABLE IF NOT EXISTS `articles` (
        `id` int NOT NULL,
        `name` varchar(255) DEFAULT NULL,
        `coordinates` varchar(45) DEFAULT NULL,
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

    names_export.export_names(cursor, 'C:\\Users\\jj\Downloads\\archive\\AgeDataset-V1.csv')

    connection.commit()
finally:
    cursor.close()
    connection.close()
