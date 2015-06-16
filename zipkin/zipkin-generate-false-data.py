import time, random, sys
import MySQLdb as mdb

def ts_microseconds():
    return int( time.time() * 1000000 )

def generate_id():
    return random.getrandbits(60)

# reference to database connector
def get_db_connection():
    return mdb.connect('localhost', 'zipkin', 'kinect', 'zipkin')

def add_span(span_name, span_id = None, trace_id = None, parent_id = None):
    global conn

    try:
        cur = conn.cursor()

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
        cur.execute(sql)


        conn.commit()

    except mdb.Error, e:
        print 'Error %d: %s' % (e.args[0], e.args[1])

    return (span_id, trace_id)

def add_annotation(span_id, trace_id, span_name, service_name, value, ipv4, port, a_timestamp, duration):
    global conn

    try:
        cur = conn.cursor()

        sql = 'INSERT INTO zipkin_annotations \
                (span_id, trace_id, span_name, service_name, value, ipv4, port, a_timestamp, duration) \
                VALUES ( \
                {span_id}, {trace_id}, \
                "{span_name}", "{service_name}", "{value}", \
                {ipv4}, {port}, {a_timestamp}, {duration})'.format(span_id=span_id, trace_id=trace_id, \
                span_name=span_name, service_name=service_name, value=value, \
                ipv4=ipv4, port=port, a_timestamp=a_timestamp, duration=duration)
        cur.execute(sql)

        conn.commit()

    except mdb.Error, e:
        print 'Error %d: %s' % (e.args[0], e.args[1])

def setup():
    global conn

    try:
        cur = conn.cursor()

        sql = 'DELETE FROM zipkin_annotations \
                WHERE trace_id IN ( \
                SELECT trace_id FROM zipkin_spans \
                WHERE span_name = "test_span")'
        cur.execute(sql)
        conn.commit()

        sql = 'DELETE FROM zipkin_spans WHERE span_name = "test_span"'
        cur.execute(sql)
        conn.commit()

    except mdb.Error, e:
        print 'Error %d: %s' % (e.args[0], e.args[1])

# get database connection
conn = get_db_connection()

setup()

span_name = 'test_span'
(span_id, trace_id) = add_span(span_name)

# print 'span_id = ', span_id , ', trace_id = ', trace_id
add_annotation(span_id, trace_id, span_name, 'test_service', 'cs', 123, 4545, 1, 0)

# print 'timestamp: ' + str(ts_microseconds())
# print 'random id: ' + str(generate_id())
