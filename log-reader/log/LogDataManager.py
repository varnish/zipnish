import varnishapi,time,os,sys,syslog,traceback

# LogDataManager responsible for recording of log data
class LogDataManager:
    def __init__(self, logStorage):
        self.logReq = {}
        self.logBereq = {}
        self.logStorage = logStorage

        self.Tags = ['ReqURL', 'BereqURL']
        self.MapTagToZipKinField = {
                'ReqURL': 'span_name',
                'BereqURL': 'span_name'
                }

    def addLogItem(self, vxid, requestType, tag, data):

        #print "type: %s, vxid: %d, tag: %s, data: %s" % (requestType, vxid, tag, data)

        if type == 'c' and tag == 'Begin':
            self.logReq = {}
            self.logBereq = {}
        elif tag == 'End':
            if requestType == 'b':
                #print self.logReq
                #print self.logBereq

                self.logStorage.push(self.logReq)
                self.logStorage.push(self.logBereq)

                self.logReq = {}
                self.logBereq = {}

        if vxid > 0:
            if (requestType == 'c' or requestType == 'b') and tag in self.Tags:
                print 'requestType: %s, tag: %s' % (requestType, tag)
                if requestType == 'c':
                    self.logReq[ self.MapTagToZipKinField[tag] ] = data.rstrip('\x00')
                elif requestType == 'b':
                    self.logBereq[ self.MapTagToZipKinField[tag] ] = data.rstrip('\x00')

    # separate, may be we can do bulk sql inserts later on
    def pushLogForVxId(self, vxid):
        # sql query for insertion
        return
