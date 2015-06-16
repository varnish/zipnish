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

'''
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
'''

def add_span(span_name, span_id = None, trace_id = None, parent_id = None):
    span_id = generate_id() if span_id is None else span_id
    parent_id = 'NULL' if parent_id is None else parent_id
    trace_id = generate_id() if trace_id is None else trace_id
    debug = 0
    duration = 0
    created_ts = ts_microseconds()

    sql = 'INSERT INTO zipkin_spans \
            (span_id, parent_id, trace_id, span_name, debug, duration, created_ts) \
            VALUES (\
            {span_id}, {parent_id}, {trace_id},\
            "{span_name}",\
            {debug},\
            {duration},\
            {created_ts}\
            )'.format(span_id=span_id, parent_id=parent_id, \
            trace_id=trace_id, span_name=span_name, debug=debug, \
            duration=duration, created_ts=created_ts)

    return (span_id, trace_id)

(span_id, trace_id) = add_span('test_span')

print 'span_id = ', span_id , ', trace_id = ', trace_id

# print 'timestamp: ' + str(ts_microseconds())
# print 'random id: ' + str(generate_id())
