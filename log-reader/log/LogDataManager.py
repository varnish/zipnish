import varnishapi,time,os,sys,syslog,traceback

# LogDataManager responsible for recording of log data
class LogDataManager:
    def __init__(self, logStorage):
        self.logRow = {}
        self.logStorage = logStorage

        self.Tags = ['ReqURL', 'BereqURL']
        self.MapTagToZipKinField = {
                'ReqURL': 'span_name',
                'BereqURL': 'span_name'
                }

    def addLogItem(self, vxid, requestType, tag, data):

        #print "type: %s, vxid: %d, tag: %s, data: %s" % (requestType, vxid, tag, data)

        if tag == 'Begin':
            self.logRow = {}
        elif tag == 'End':
            self.logRow['request_type'] = requestType
            self.logStorage.push(self.logRow)
            self.logRow = {}

        if tag in self.Tags:
            self.logRow[ self.MapTagToZipKinField[tag] ] = data.rstrip('\x00')

    # separate, may be we can do bulk sql inserts later on
    def pushLogForVxId(self, vxid):
        # sql query for insertion
        return
