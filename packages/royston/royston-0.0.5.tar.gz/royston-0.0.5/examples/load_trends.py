"""
Simple routine to run a query on a database and print the results:

Train the data to a local pickle file
"""
from royston.royston import Royston
from datetime import datetime as dt
import pytz
import pickle

from dateutil.parser import parse


# load data file


roy = pickle.load( open( "roy.pickle", "rb" ) )

trends = roy.trending()
print(trends)
