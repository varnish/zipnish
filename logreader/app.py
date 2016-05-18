#!/usr/bin/env python

import ConfigParser
import logging
import os
import signal
import sys
import threading

import varnishapi
from _mysql_exceptions import OperationalError
from log.db import LogDatabase
from log.log_snapshot import Snapshot
from log.parser import (
    annotations,
    clear_annotations,
    clear_spans,
    parse_log_row,
    spans,
)


log = logging.getLogger()
snapshot = Snapshot()
config = ConfigParser.ConfigParser()
__DB_PARAMS__ = dict()


LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR}

varnish_log_args = ['-g', 'request']
callback_sleep_time = 0.5
cache_name = None

storage = None
vap = None
task = None


def init_log():
    log_file = config.get('Log', 'log_file')
    log_level = config.get('Log', 'log_level')
    log_format = '%(asctime)s %(levelname)s: %(message)s ' \
                 '[in %(pathname)s:%(lineno)d]'

    try:
        logging.basicConfig(level=LEVELS.get(log_level.lower()),
                            format=log_format,
                            filename=log_file,
                            filemode='w')
    except IOError as io:
        print io.message
        sys.exit(1)
    except Exception as ex:
        print ex.args[0]
        sys.exit(1)


def init_config(overridden_config=None):

    # The directory of the script.
    default_config = os.path.join(
        os.path.dirname(sys.argv[0]), "default.cfg")

    etc_config = os.path.join("/etc/zipnish/zipnish.cfg")

    # ~/.
    extra_cfg_files = [default_config, etc_config]

    if overridden_config:
        extra_cfg_files.append(os.path.join(os.getcwd(), overridden_config))

    for f in extra_cfg_files:
        if os.path.isfile(f):
            with open(f) as fp:
                config.readfp(fp)
                break

    config.read(extra_cfg_files)
    try:
        assert config.has_section('Database'), "Database section is missing."
        assert config.has_option(
            'Database', 'host'), "MySql host option is missing."
        assert config.has_option(
            'Database', 'db_name'), "MySql database name option is missing."
        assert config.has_option(
            'Database', 'user'), "MySql user option is missing."
        assert config.has_option(
            'Database', 'pass'), "MySql password option is missing."
        assert config.has_section('Log'), "Log section missing."
        assert config.has_option(
            'Log', 'log_file'), "Log file path is missing."
        assert config.has_option(
            'Log', 'log_level'), "Log level option is missing."
    except AssertionError as ae:
        print ae.message
        sys.exit(1)

    __DB_PARAMS__['host'] = config.get('Database', 'host')
    __DB_PARAMS__['db'] = config.get('Database', 'db_name')
    __DB_PARAMS__['user'] = config.get('Database', 'user')
    __DB_PARAMS__['passwd'] = config.get('Database', 'pass')
    __DB_PARAMS__['keep_alive'] = config.get('Database', 'keep_alive')

    if config.has_option('Sync', 'splay'):
        global callback_sleep_time
        callback_sleep_time = config.getfloat('Sync', 'splay')

    if config.has_option('Cache', 'name'):
        global cache_name
        cache_name = config.get('Cache', 'name')


def vap_callback(vap, cbd, priv):
    try:
        vxid = cbd['vxid']
        request_type = cbd['type']
        tag = cbd['tag']
        t_tag = vap.VSL_tags[tag]
        data = cbd['data']
        snapshot.fill_snapshot(vxid, request_type, t_tag, data)
    except Exception as vap_callback_ex:
        log.error(vap_callback_ex)


def error_callback(error):
    log.error(error)
    vap.Fini()


def fetch_varnish_log():
    out = vap.Dispatch(vap_callback)
    interval = 0
    if not out:
        interval = 0.5  # callback_sleep_time
    task.interval = interval


class PeriodicEvent(object):

    def __init__(self, interval, func):
        self.interval = interval
        self.func = func
        self.terminate = threading.Event()

    def _signals_install(self, func):
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, func)

    def _signal_handler(self, signum, frame):
        self.terminate.set()

    def run(self):
        self._signals_install(self._signal_handler)
        while not self.terminate.is_set():
            self.func()
            self.terminate.wait(self.interval)
        self._signals_install(signal.SIG_DFL)


def snapshot_callback(log_input):
    parse_log_row(log_input)

    if len(annotations) >= 4:
        storage.insert("spans", spans)
        storage.insert("annotations", annotations)
        clear_spans()
        clear_annotations()


def main():
    global storage
    global vap
    global task

    init_config()
    init_log()

    try:
        storage = LogDatabase(**__DB_PARAMS__)
        if cache_name:
            varnish_log_args.extend(['-n', cache_name])
        snapshot.add_callback_func(snapshot_callback)

        vap = varnishapi.VarnishLog(varnish_log_args)
        task = PeriodicEvent(0.5, fetch_varnish_log)
        log.debug("Log Reader is about to start.")
        task.run()
    except OperationalError as op:
        print "Database error %s" % op.args[0]
        log.error(op)
    except Exception as ex:
        print "Unknown exception %s" % ex.args[0]
        log.error(ex)


if __name__ == '__main__':
    main()
