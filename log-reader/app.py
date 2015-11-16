import ConfigParser
import logging
import os
import sys

import varnishapi
from log.LogDataManager import LogDataManager
from log.LogDatabase import LogDatabase
from log.LogReader import CallbackRunner
from log.LogStorage import LogStorage


log = logging.getLogger()

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR}

config = ConfigParser.ConfigParser()

# default connection parameters to database
__DB_PARAMS__ = {
    'host': '192.168.75.12',
    'db': 'microservice',
    'user': 'microservice',
    'passwd': 'WqPv5fBSLgnskM7',
    'keep_alive': True,
    'truncate_tables': False
}

varnish_log_args = ['-g', 'request']
callback_sleep_time = 0.5
cache_name = None


def init_log():
    log_file = config.get('Log', 'log_file')
    log_level = config.get('Log', 'log_level')
    log_format = '%(asctime)s %(levelname)s: %(message)s ' \
                 '[in %(pathname)s:%(lineno)d]'

    logging.basicConfig(level=LEVELS.get(log_level.lower()),
                        format=log_format,
                        filename=log_file,
                        filemode='w')


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
    assert config.has_option('Log', 'log_file'), "Log file path is missing."
    assert config.has_option(
        'Log', 'log_level'), "Log level option is missing."

    __DB_PARAMS__['host'] = config.get('Database', 'host')
    __DB_PARAMS__['db'] = config.get('Database', 'db_name')
    __DB_PARAMS__['user'] = config.get('Database', 'user')
    __DB_PARAMS__['passwd'] = config.get('Database', 'pass')

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
        log_data_manager.addLogItem(vxid, request_type, t_tag, data)
    except Exception as vap_callback_ex:
        log.error(vap_callback_ex)


def error_callback(error):
    log.error(error)
    vap.Fini()


def fetch_varnish_log(vap):
    out = vap.Dispatch(vap_callback)
    interval = 0
    if not out:
        interval = callback_sleep_time
    callback_runner.set_interval(interval)


if __name__ == '__main__':
    init_config()
    init_log()

    if cache_name:
        varnish_log_args.extend(['-n', cache_name])
    vap = varnishapi.VarnishLog(varnish_log_args)

    callbacks = [fetch_varnish_log]
    callback_runner = CallbackRunner(callbacks, error_callback, vap)

    try:
        log_database = LogDatabase(**__DB_PARAMS__)
        log_storage = LogStorage(log_database)
        log_data_manager = LogDataManager(log_storage)
    except Exception as e:
        log.error(e)
        print "Error occurred: %s" % e.args[0]
        sys.exit(-1)

    log_cache_name = "default" if not cache_name else cache_name
    log.info("Starting log reader for cache: %s" % log_cache_name)
    callback_runner.run()

    raw_input("Press Enter to stop the sharade.\n")
    log.info("Log reader has stopped.")
