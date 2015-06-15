import time
import random

import MySQLdb

def ts_microseconds():
    return int( time.time() * 1000000 )

def generate_id():
    return random.getrandbits(64)

# reference to database connector
def get_db_connection():
    return MySQLdb.connect('localhost', 'zipkin', 'kinect', 'zipkin')

db = get_db_connection()

print db


# print 'timestamp: ' + str(ts_microseconds())
# print 'random id: ' + str(generate_id())
