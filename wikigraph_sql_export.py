import csv
import mysql.connector

def export_wikigraph(cursor, path):
    with open(path, 'r', newline='', encoding="utf8") as f:
        reader = csv.DictReader(f, delimiter='\t')
        count = 0
        for row in reader:
            if count >= 10000:
                break
            from_id = int(row['page_id_from'])
            to_id = int(row['page_id_to'])
            from_name = row['page_title_from']
            to_name = row['page_title_to']
            print(from_id, to_id, from_name, to_name)
            cursor.execute(
                "INSERT INTO links (from_id, to_id, from_name, to_name) VALUES (%s, %s, %s, %s)",
                (from_id, to_id, from_name, to_name)
            )
            count += 1
        f.close()