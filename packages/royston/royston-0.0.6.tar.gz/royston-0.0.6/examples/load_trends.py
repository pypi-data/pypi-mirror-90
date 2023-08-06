"""
Think about the demo:

how do we do it?
How do we tell a trend from something that is mentioned a lot?
search ui - simple phrases and it does a keyword search for stories and show the trend line
Hard code subjects?


UI:

click hides the popup


Show long tail terms :)




for a model, we want the following:

    list subjects

API:

- trends per subject

"""

"""
Simple routine to run a query on a database and print the results:

Train the data to a local pickle file
"""
from royston.royston import Royston
from datetime import datetime as dt
import pytz
import pickle

from dateutil.parser import parse

import json







"""
Simple routine to run a query on a database and print the results:

Train the data to a local pickle file
"""
from royston.royston import Royston
from datetime import datetime as dt
import pytz
import pickle
import psycopg2
import json

conn = psycopg2.connect(
    host="tickerpipe.com",
    database="news",
    user="news_user",
    password="asfjaofjifjsf")

def load_articles(conn, ids):

    ids_str = "', '".join(ids)
    cur = conn.cursor()
    cur.execute( "SELECT id, title, published_date, site_id FROM article WHERE id IN ('" + ids_str + "')")
    return cur.fetchall()


def get_article(articles, id):

    for article in articles:
        if article[0] == id:
            return article
    

# load data file
roy = pickle.load( open( "roy.pickle", "rb" ) )
roy.set_options({ 'trends_top_n': 15 })
trends = roy.trending()

# first thing - get all the doc ids
doc_ids = []
for trend in trends:
    doc_ids = doc_ids + trend['docs']

articles = load_articles(conn, doc_ids)

#export const data = [ { name:

trend_json = []

# format the trends:
for trend in trends:
    print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
    print(trend['phrases'])

    print(json.dumps(trend['phrases']))

    name = json.dumps(trend['phrases'])
    events = []

    for doc_id in trend['docs']:
        article = get_article(articles, doc_id)
        events.append({ 'date': article[2], 'data': { 'body': article[1] }})

    trend_json.append({ 'name': name, 'events': events })

print("export const data = "+json.dumps(trend_json, indent=4, sort_keys=True, default=str))


# write to a file

f = open("/Users/ian/Dev/charts/src/charts/news-data.js", "w")
f.write("export const data = "+json.dumps(trend_json, indent=4, sort_keys=True, default=str))
f.close()


"""
    for doc in trend['docs']:
        title, published_date, site_id = load_article(conn, doc)
        print(title, published_date, site_id)
"""

# do the thing to remove all count of 1 or 2 from the history
conn.close()
























