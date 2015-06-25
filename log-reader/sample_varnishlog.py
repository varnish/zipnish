import varnishapi,time,os,sys,syslog,traceback

# LogDataManager responsible for recording of log data
class LogDataManager:
    def __init__(self):
        self.sessionVxId = 0;
        self.logSessions = {}

    def addLogItem(self, vxid, tag, data):
        print "sessionId: %d, vxid: %d, tag: %s, data: %s" % (self.sessionVxId, vxid, tag, data)

        if tag == 'SessOpen':
            self.sessionVxId = vxid
        elif tag == 'SessClose':
            self.pushLog(self.sessionVxId)

            # reset to 0
            # new session will automatically set a new sessionVxId
            self.sessionVxId = 0;

    def pushLog(self):
        self.pushLogForVxId(self.sessionVxId)

    # separate, may be we can do bulk sql inserts later on
    def pushLogForVxId(self, vxid):
        # sql query for insertion
        return

# LogReader - read and do basic processing of incoming data
class LogReader:
    def __init__(self, logDataManager):
        self.logDataManager = logDataManager

    def execute(self,vap):
        #connect varnishapi
        self.vap = vap
        while 1:
            ret = self.vap.Dispatch(self.vapCallBack)
            if 0 == ret:
                time.sleep(0.5)

    def vapCallBack(self,vap,cbd,priv):
        # unique / request
        vxid = cbd['vxid']

        # tag, will be a number
        tag = cbd['tag']

        # text version of the tag above
        t_tag = vap.VSL_tags[tag]

        # log data
        data = cbd['data']

        # push to logDataManager for storage
        self.logDataManager.addLogItem(vxid, t_tag, data);

# called when the program starts up
def main(sharedMemoryLog):
    try:
        # connect to varnish log
        vap = varnishapi.VarnishLog()

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
