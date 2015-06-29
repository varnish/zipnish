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
        elif tag == 'ReqHeader' or tag == 'BereqHeader':
            split = data.split(': ')
            value = split[1].rstrip('\x00')

            if split[0] == 'X-Varnish':
                self.logRow['span_id'] = value
                self.logRow['trace_id'] = value
            elif split[0] == 'X-Varnish-Parent':
                self.logRow['parent_id'] = value
            elif split[0] == 'Host':
                ipv4 = value
                port = 0

                if value.find(':') > -1:
                    value = value.split(':')
                    ipv4 = value[0]
                    port = value[1]

                self.logRow['ipv4'] = ipv4
                self.logRow['port'] = port

                print tag + ': ' + split[1]

    # separate, may be we can do bulk sql inserts later on
    def pushLogForVxId(self, vxid):
        # sql query for insertion
        return
