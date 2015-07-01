# basic stuff required for logging / debugging
import os, sys, syslog, traceback

# varnishapi to interact with varnishlog
import varnishapi

# log module to manage data flow coming in from varnishlog into ZipKin database
from log import LogReader, LogDataManager, LogStorage

# called when the program starts up
def main(sharedMemoryLog):
    try:
        # connect to varnish log
        vap = varnishapi.VarnishLog(['-g', 'request'])

        # connect to varnishapi and begin logging
        # logDataManager
        sharedMemoryLog.execute(vap)

    # keyboard exception
    except KeyboardInterrupt:
        vap.Fini()

    # log exception at system level
    except Exception as e:
        syslog.openlog(sys.argv[0], syslog.LOG_PID | syslog.LOG_PERROR, syslog.LOG_LOCAL0)
        syslog.syslog(syslog.LOG_ERR, traceback.format_exc())

if __name__ == '__main__':
    # log data storage
    logStorage = LogStorage()

    # manages log data
    logDataManager = LogDataManager(logStorage)

    # shared memory log reader
    shmLog = LogReader(logDataManager)

    # initiate logging
    main(shmLog)
