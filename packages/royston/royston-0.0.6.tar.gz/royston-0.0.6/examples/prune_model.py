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


roy = pickle.load( open( "roy.small.pickle", "rb" ) )

print('loaded!')
roy.prune()
print('pruned!')


pickle.dump(roy, open("roy.small.pruned.pickle", "wb" ))
