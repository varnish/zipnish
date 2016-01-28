import sys
import threading
import time
import unittest
import requests

from multiprocessing import Process
from unittest import TestCase
from server import (
    ServerHandler,
    ThreadedHTTPServer,
    load_yaml_config,
    trace_urls,
)
try:
    sys.path.append("..")
    import varnishapi
    from log.LogDataManager import LogDataManager
    from log.LogDatabase import LogDatabase
    from log.LogStorage import LogStorage
except ImportError as ex:
    print "Import error: %s" % ex
    sys.exit(1)


PORT = 9999
HOST = '127.0.0.1'

VARNISH_PORT = 6081

__DB_PARAMS__ = {
    'host': '192.168.75.12',
    'db': 'microservice',
    'user': 'microservice',
    'passwd': 'WqPv5fBSLgnskM7',
    'keep_alive': True,
    'truncate_tables': False
}

log_database = LogDatabase(**__DB_PARAMS__)
log_storage = LogStorage(log_database)
log_storage.minNumOfSpansToFlush = 24
log_storage.minNumOfAnnotationsToFlush = 2 * log_storage.minNumOfSpansToFlush
log_data_manager = LogDataManager(log_storage)
vap = varnishapi.VarnishLog(['-g', 'request'])


def start_test_server():
    server = ThreadedHTTPServer((HOST, PORT), ServerHandler)
    server.serve_forever()


def vap_callback(vap, cbd, priv):
    try:
        vxid = cbd['vxid']
        request_type = cbd['type']
        tag = cbd['tag']
        t_tag = vap.VSL_tags[tag]
        data = cbd['data']
        log_data_manager.add_log_item(vxid, request_type, t_tag, data)
    except Exception as vap_callback_ex:
        print vap_callback_ex


def run_cb():
    while True:
        ret = vap.Dispatch(vap_callback)
        if not ret:
            time.sleep(0.5)


class BasicTestCase(TestCase):

    def test_log_reader(self):
        """
        This test requires that varnish is up and running under
        the <VARNISH_PORT> and has as a backend the test server
        spawned with <HOST> and <PORT>.
        """
        load_yaml_config()
        self.assertEqual(1, len(trace_urls))

        server_process = Process(target=start_test_server)
        server_process.start()

        t = threading.Thread(target=run_cb, args=())
        t.daemon = True
        t.start()

        req_url = "http://%s:%s%s" % (HOST, VARNISH_PORT, trace_urls[0])
        requests.get(req_url)

        server_process.join(timeout=1)
        server_process.terminate()
        t.join(1)

        self.assertEqual(len(log_storage.spans), 16)
        self.assertEqual(len(log_storage.annotations), 32)


if __name__ == '__main__':
    unittest.main()
