"""
Simple routine to run a query on a database and print the results:

Train the data to a local pickle file
"""
from royston.royston import Royston
from datetime import datetime as dt
import pytz
import pickle

def clean_train():

    # count how many documents to ingest
    offset = 0
    step = 50

def train( conn ) :

    cur = conn.cursor()

    cur.execute( "SELECT article.id, article.title, published_date, site.subject_id AS subject_id FROM article INNER JOIN site ON site.id = article.site_id WHERE published_date >= date_trunc('month', current_date - interval '3' month)" )

    # just the last week: cur.execute( "SELECT article.id, article.title, published_date, site.subject_id AS subject_id FROM article INNER JOIN site ON site.id = article.site_id WHERE published_date >= date_trunc('month', current_date - interval '7' day) ORDER BY published_date DESC LIMIT 5000" )

    roy = Royston()
    for id, title, published_date, subject_id in cur.fetchall() :
        #print (id, title, published_date, subject_id)
        # ingest a few documents
        roy.ingest({ 'id': id, 'body': title, 'date': published_date })

    # find the trends - with this example, it won't find anything, as it's only got two stories!
    trends = roy.trending()
    print(trends)
    pickle.dump(roy, open("roy.pickle", "wb" ))




print( "Using psycopg2:" )
import psycopg2

conn = psycopg2.connect(
    host="tickerpipe.com",
    database="news",
    user="news_user",
    password="asfjaofjifjsf")
print( "connected psycopg2:" )

# do the thing to remove all count of 1 or 2 from the history
train(conn)
conn.close()

