import varnishapi,time,os,sys,syslog,traceback

# LogDataManager responsible for recording of log data
class LogDataManager:
    def __init__(self):
        self.logReq = {}
        self.logBereq = {}

    def addLogItem(self, vxid, requestType, tag, data):

        print "type: %s, vxid: %d, tag: %s, data: %s" % (requestType, vxid, tag, data)

        if type == 'c' and tag == 'Begin':
            self.logReq = {}
            self.logBereq = {}
        elif tag == 'End':
            if requestType == 'b':
                #print self.logReq
                #print self.logBereq

                self.logBereq = {}
                self.logReq = {}

        if vxid > 0:
            if requestType == 'b':
                self.logReq[tag] = data.rstrip('\x00')
            elif requestType == 'c':
                self.logBereq[tag] = data.rstrip('\x00')

    # separate, may be we can do bulk sql inserts later on
    def pushLogForVxId(self, vxid):
        # sql query for insertion
        return
