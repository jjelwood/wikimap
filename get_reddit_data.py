import praw
import json

config = json.load(open("config.json"))

reddit= praw.Reddit(
    client_id=config["reddit_client_id"],
    client_secret=config["reddit_client_secret"],
    user_agent=config["reddit_user_agent"]

)


def get_reddit_data(cursor):
    cursor.execute(f"SELECT name FROM articles")
    rows = cursor.fetchall()
    for row in rows:
        person_name = row[0]
        inserted=0
        submissions=reddit.subreddit("all").search(person_name,limit=10)
        for submission in submissions:
            if not submission.over_18:
                query = f"INSERT INTO posts (name,submission_id, submission_title,submission_url, submission_score, submission_author) VALUES (%s,%s,%s,%s,%s,%s)" 
                cursor.execute(query,(person_name,submission.id,submission.title,submission.url,submission.score,submission.author.name) )
                inserted=1
                break
            else:
                continue
        if inserted==0:
            query = f"INSERT INTO posts (name,submission_id, submission_title,submission_url, submission_score, submission_author) VALUES (%s,%s,%s,%s,%s,%s)" 
            cursor.execute(query,(person_name,None,None,None,None,None) )
        
        
        
        


