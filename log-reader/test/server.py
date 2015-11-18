#!/usr/bin/python

import random
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn

import requests
import yaml


PORT = 9999
HOST = '127.0.0.1'
VARNISH_PORT = 6081

trace_urls = []
all_spans = []
yaml_config = dict()
trace_spans = dict()
span_sleep = dict()


def load_yaml_config():
    with open("server.yaml", 'r') as stream:
        yaml_config.update((yaml.load(stream)))
        for trace in yaml_config.values():
            for trace_meta in trace:
                trace_url = trace_meta.get('trace')[0].get('url')
                trace_urls.append(trace_url)
                spans = trace_meta.get('trace')[1:]
                trace_spans[trace_url] = spans
                all_spans.extend([x['span'] for x in spans])

        for span in all_spans:
            sleep_int = random.randint(1, 10)
            sleep = float(sleep_int) / 10
            time.sleep(sleep)
            span_sleep[span] = sleep

        for trace_url in trace_urls:
            sleep_int = random.randint(1, 10)
            sleep = float(sleep_int) / 10
            time.sleep(sleep)
            span_sleep[trace_url] = sleep


class ServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        x_varnish_header = self.headers['x-varnish']
        trace_header = x_varnish_header

        if 'x-varnish-trace' in self.headers:
            trace_header = self.headers['x-varnish-trace']

        headers = {'x-varnish-trace': trace_header,
                   'x-varnish-parent': x_varnish_header}

        sleep_time = span_sleep[self.path]
        time.sleep(sleep_time)

        if self.path in trace_spans.keys():
            for span in trace_spans[self.path]:
                url = span['span']
                req_url = "http://%s:%s%s" % (HOST, VARNISH_PORT, url)
                requests.get(req_url, headers=headers)
            self.send_response(200)
        elif self.path in all_spans:
            self.send_response(200)
        else:
            self.send_response(404)

        self.send_header('Content-type', 'text/html')
        self.end_headers()


def get_total_sleep_time():
    return sum(span_sleep.values())


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


def start_server():
    server = None
    try:
        server = ThreadedHTTPServer((HOST, PORT), ServerHandler)
        print "Started test server on port %s" % PORT
        server.serve_forever()
    except KeyboardInterrupt:
        print " received, stopping server..."
    finally:
        if server:
            server.socket.close()
        print "Server stopped."
        print get_total_sleep_time()

if __name__ == '__main__':
    load_yaml_config()
    start_server()
