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
                WHERE span_name IN ("test_span", "test_span_child"))'
        cur.execute(sql)
        conn.commit()

        sql = 'DELETE FROM zipkin_spans \
                WHERE span_name IN \
                ("test_span", "test_span_child") \
                '
        cur.execute(sql)
        conn.commit()

    except mdb.Error, e:
        print 'Error %d: %s' % (e.args[0], e.args[1])

# get database connection
conn = get_db_connection()

setup()

span_name = 'test_span'
child_span_name = 'test_span_child'

span_service = 'test_service'
span_child_service = 'test_child_service'

# start a trace by adding a parent span
(span_id, trace_id) = add_span(span_name)

# add server sent annotation to a parent span
add_annotation(span_id, trace_id, span_name, span_service, 'sr', 714278707, 2974, 1434511563438000, 0)

# add child span
(child_span_id, trace_id) = add_span(child_span_name, None, trace_id, span_id)

# add child span annotations (client send, server receive, server sent, client receive)
add_annotation(child_span_id, trace_id, child_span_name, span_child_service, 'cs', 2133576259, 8029, 1434511563545000, 0)
add_annotation(child_span_id, trace_id, child_span_name, span_child_service, 'sr', 2133576259, 8029, 1434511563547000, 0)
add_annotation(child_span_id, trace_id, child_span_name, span_child_service, 'ss', 2133576259, 8029, 1434511563549000, 0)
add_annotation(child_span_id, trace_id, child_span_name, span_child_service, 'cr', 2133576259, 8029, 1434511563553000, 0)

# add server recieve annotation for the parent span
add_annotation(span_id, trace_id, span_name, 'test_service', 'ss', 714278707, 2974, 1434511563558000, 0)
