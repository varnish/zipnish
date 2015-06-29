import varnishapi,time,os,sys,syslog,traceback

# LogDataManager responsible for recording of log data
class LogDataManager:
    def __init__(self, logStorage):
        self.logReq = {}
        self.logBereq = {}
        self.logStorage = logStorage

        self.Tags = ['ReqURL', 'BereqURL', 'ReqHeader', 'BereqHeader']
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
                if tag == 'ReqHeader' or tag == 'BereqHeader':
                    split = data.split(': ')

                    if split[0] == 'X-Varnish':
                        self.logReq['span_id'] = split[1].rstrip('\x00')
                        self.logBereq['trace_id'] = self.logReq['span_id']
                    #print tag + ' - ' + split[0] + ' -> ' + split[1]
                elif requestType == 'c':
                    self.logReq[ self.MapTagToZipKinField[tag] ] = data.rstrip('\x00')
                elif requestType == 'b':
                    self.logBereq[ self.MapTagToZipKinField[tag] ] = data.rstrip('\x00')

    # separate, may be we can do bulk sql inserts later on
    def pushLogForVxId(self, vxid):
        # sql query for insertion
        return
