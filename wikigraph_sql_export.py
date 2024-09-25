import csv
import mysql.connector

def export_wikigraph(cursor, path):
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f, delimiter='\t')
        count = 0
        for row in reader:
            count += 1
            if count >= 10000:
                break
            from_id = int(row['from_id'])
            to_id = int(row['to_id'])
            from_name = row['from_name']
            to_name = row['to_name']
            link_id = 
            cursor.execute(f"INSERT INTO `links` (id, from_id, to_id, from_name, to_name) VALUES ({row[]})")