import mysql.connector
import wikigraph_sql_export

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password"
)

cursor = db.cursor()

cursor.execute("CREATE DATABASE wikigraph")

cursor.execute("USE wikigraph")

if cursor.execute("SHOW TABLES LIKE 'articles'") != 1:
    cursor.execute("""CREATE TABLE `articles` (
        `id` int NOT NULL,
        `name` varchar(45) DEFAULT NULL,
        `coordinates` varchar(45) DEFAULT NULL,
        `url` varchar(45) DEFAULT NULL,
        `length` int DEFAULT NULL,
        `citations` int DEFAULT NULL,
        `edits` int DEFAULT NULL,
        `editors` int DEFAULT NULL,
        `created` datetime DEFAULT NULL,
        `pagerank` decimal(10,0) DEFAULT NULL,
        `reputability_score` decimal(10,0) DEFAULT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """)

if cursor.execute("SHOW TABLES LIKE 'comments'") != 1:
    cursor.execute("""CREATE TABLE `comments` (
        `id` int NOT NULL AUTO_INCREMENT,
        `article_id` int DEFAULT NULL,
        `article_name` varchar(45) DEFAULT NULL,
        `text` varchar(45) DEFAULT NULL,
        `date` datetime DEFAULT NULL,
        `username` varchar(45) DEFAULT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """)

if cursor.execute("SHOW TABLES LIKE 'links'") != 1:
    cursor.execute("""CREATE TABLE `links` (
        `id` int NOT NULL,
        `from_id` int DEFAULT NULL,
        `to_id` int DEFAULT NULL,
        `from_name` varchar(45) DEFAULT NULL,
        `to_name` varchar(45) DEFAULT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """)

