import time
import random

import sys
import MySQLdb as mdb

def ts_microseconds():
    return int( time.time() * 1000000 )

def generate_id():
    return random.getrandbits(64)

# reference to database connector
def get_db_connection():
    return mdb.connect('localhost', 'zipkin', 'kinect', 'zipkin')

conn = get_db_connection()

try:
    cur = conn.cursor()
    cur.execute('SELECT VERSION()')

    ver = cur.fetchone()

    print 'Database version: %s ' % ver

except mdb.Error, e:
    print 'Error %d: %s' % (e.args[0], e.args[1])
    sys.exit(1)

finally:

    if conn:
        conn.close()

# print 'timestamp: ' + str(ts_microseconds())
# print 'random id: ' + str(generate_id())
