import unittest
from multiprocessing import Process
from unittest import TestCase

import requests
from server import (
    ServerHandler,
    ThreadedHTTPServer,
    get_total_sleep_time,
    load_yaml_config,
    trace_urls,
)
from simplemysql import SimpleMysql


# Port to be used by the test server.
PORT = 9999

# Host used be the test server.
# Do note that for the test to work, it is required
# that the test server is set as a backend
# in your vcl configuration
HOST = '127.0.0.1'

# The port where varnish is exposed.
VARNISH_PORT = 6081

__DB_PARAMS__ = {
    'host': '192.168.75.12',
    'db': 'microservice',
    'user': 'microservice',
    'passwd': 'WqPv5fBSLgnskM7'
}


def start_server():
    server = ThreadedHTTPServer((HOST, PORT), ServerHandler)
    server.serve_forever()


def run_sql(query, *args):
    db = SimpleMysql(**__DB_PARAMS__)
    db.query(query, args)
    db.commit()
    db.conn.close()


def get_timestamp(timestamp_order):
    db = SimpleMysql(**__DB_PARAMS__)
    cursor = db.query("select created_ts from zipnish_spans "
                      "order by created_ts %s limit 1" % timestamp_order)

    ts = cursor.fetchone()[0]
    cursor.close()
    db.conn.close()
    return ts


class LogReaderTestCase(TestCase):

    def setUp(self):
        run_sql("DELETE FROM zipnish_annotations")
        run_sql("DELETE FROM zipnish_spans")

    def test_serial_call_response_times(self):
        load_yaml_config()
        self.assertEqual(1, len(trace_urls))

        total_sleep_time = int(get_total_sleep_time() * 1000)
        server_process = Process(target=start_server)
        server_process.start()

        req_url = "http://%s:%s%s" % (HOST, VARNISH_PORT, trace_urls[0])
        requests.get(req_url)

        server_process.join(timeout=1)
        server_process.terminate()

        max = get_timestamp("DESC")
        min = get_timestamp("ASC")

        delta = (max - min) / 1000
        self.assertAlmostEqual(delta, total_sleep_time, delta=150)


if __name__ == '__main__':
    unittest.main()
