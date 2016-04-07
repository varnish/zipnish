import sys
import threading
import time
import unittest
from multiprocessing import Process
from unittest import TestCase

import requests
from server import (
    ServerHandler,
    ThreadedHTTPServer,
    load_yaml_config,
    trace_urls,
)


try:
    sys.path.append("..")
    import varnishapi
    from log.LogDatabase import LogDatabase
    from log.log_snapshot import Snapshot
    from log.parser import parse_log_row, spans, annotations
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

_vap = varnishapi.VarnishLog(['-g', 'request'])
_log_database = LogDatabase(**__DB_PARAMS__)
_snapshot = Snapshot()
_snapshot.add_callback_func(parse_log_row)


def _vap_callback(vap, cbd, priv):
    lock = threading.Lock()
    try:
        lock.acquire()
        vxid = cbd['vxid']
        request_type = cbd['type']
        tag = cbd['tag']
        t_tag = vap.VSL_tags[tag]
        data = cbd['data']
        _snapshot.fill_snapshot(vxid, request_type, t_tag, data)
    except KeyError as key_error:
        print "Key error occured: ", key_error.message
    except Exception as vap_callback_ex:
        print vap_callback_ex
    finally:
        lock.release()


def clear_log_storage():
    assert _snapshot
    del spans[:]
    del annotations[:]


class BaseTestCase(TestCase):

    __test__ = False

    def __start_test_server():
        server = ThreadedHTTPServer((HOST, PORT), ServerHandler)
        server.serve_forever()

    server_process = Process(target=__start_test_server)

    def __run_cb(self):
        assert _vap
        while True:
            ret = _vap.Dispatch(_vap_callback)
            if not ret:
                time.sleep(0.5)

    @classmethod
    def setUpClass(cls):
        assert cls.server_process
        load_yaml_config()

        cls.server_process.daemon = True
        cls.server_process.start()

    @classmethod
    def tearDownClass(cls):
        cls.server_process.terminate()
        cls.server_process.join(timeout=1)

        assert not cls.server_process.is_alive()

    def setUp(self):
        clear_log_storage()

    def run_test_requests(self):
        """
        This method requires that varnish is up and running under
        the <VARNISH_PORT> and has as a backend the test server
        spawned with <HOST> and <PORT>.
        """
        vap_binding_cb_thread = threading.Thread(target=self.__run_cb)
        vap_binding_cb_thread.daemon = True
        vap_binding_cb_thread.start()

        req_url = "http://%s:%s%s" % (HOST, VARNISH_PORT, trace_urls[0])
        requests.get(req_url)

        vap_binding_cb_thread.join(1)


class LogReaderTestCase(BaseTestCase):

    def assert_dict(self, dict_def, dict_values):
        assert isinstance(dict_def, dict)
        assert isinstance(dict_values, dict)

        self.assertEqual(set(dict_def.keys()),
                         set(dict_values.keys()))
        for k, v in dict_values.items():
            self.assertIsNotNone(dict_values[k])
            self.assertIsInstance(v, dict_def[k])

    def test_span_and_annotation_count(self):
        self.run_test_requests()
        self.assertEqual(len(spans), 16)
        self.assertEqual(len(annotations), 32)

    def test_span_dict_structure(self):
        self.run_test_requests()

        span_def = {'span_id': str,
                    'parent_id': str,
                    'trace_id': str,
                    'span_name': str,
                    'debug': int,
                    'duration': int,
                    'created_ts': int}

        for span in spans:
            self.assert_dict(span_def, span)

    def test_annotation_dict_structure(self):
        self.run_test_requests()
        annotation_def = {'span_id': str,
                          'trace_id': str,
                          'span_name': str,
                          'service_name': str,
                          'value': str,
                          'ipv4': int,
                          'port': str,
                          'a_timestamp': int,
                          'duration': int}

        for annotation in annotations:
            self.assert_dict(annotation_def, annotation)


if __name__ == '__main__':
    unittest.main()
