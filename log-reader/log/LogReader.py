# basic stuff required for logging / debugging
import os, sys, syslog, traceback

import time

# LogReader - read and do basic processing of incoming data
class LogReader:
    def __init__(self, logDataManager):
        self.logDataManager = logDataManager

    def execute(self,vap):
        #connect varnishapi
        self.vap = vap
        while 1:
            try:
                ret = self.vap.Dispatch(self.vapCallBack)
                if 0 == ret:
                    time.sleep(0.5)
            except Exception as e:
                # send pass on this exception because
                # sometimes varnish can restart or some reader share memory log is un-reachable
                pass
                # syslog.openlog(sys.argv[0], syslog.LOG_PID | syslog.LOG_PERROR, syslog.LOG_LOCAL0)
                # syslog.syslog(syslog.LOG_ERR, traceback.format_exc())

    def vapCallBack(self,vap,cbd,priv):
        # unique / request
        vxid = cbd['vxid']

        # request type
        requestType = cbd['type']

        # tag, will be a number
        tag = cbd['tag']

        # text version of the tag above
        t_tag = vap.VSL_tags[tag]

        # log data
        data = cbd['data']

        # push to logDataManager for storage
        self.logDataManager.addLogItem(vxid, requestType, t_tag, data);
