import varnishapi,os,sys,syslog,traceback
from log import LogReader, LogDataManager

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
    # manages log data
    logDataManager = LogDataManager()

    # shared memory log reader
    shmLog = LogReader(logDataManager)

    # initiate logging
    main(shmLog)
