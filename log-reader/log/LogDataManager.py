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

        # print "type: %s, vxid: %d, tag: %s, data: %s" % (requestType, vxid, tag, data)

        if tag == 'Begin':
            self.logRow = {}
            self.logRow['begin'] = data

        elif tag == 'End':
            self.logRow['request_type'] = requestType
            self.logStorage.push(self.logRow)

            self.logRow = {}


        if tag in self.Tags:
            self.logRow[ self.MapTagToZipKinField[tag] ] = data.rstrip('\x00')

        elif tag == 'Link':
            value = data.rstrip('\x00')
            value = value[6:]
            value = value[:value.find(' ')].strip(' ')

            self.logRow['link'] = value

        elif tag == 'Timestamp':
            split = data.split(': ', 1)
            timestamp = split[1].rstrip('\x00')
            timeValues = timestamp.split(' ')

            self.logRow['timestamp-abs-' + split[0]] = timeValues[0]
            self.logRow['timestamp-duration-' + split[0]] = timeValues[2]

        elif tag == 'ReqHeader' or tag == 'RespHeader' or tag == 'BereqHeader' or tag == 'BerespHeader':
            split = data.split(': ', 1)
            value = split[1].rstrip('\x00')

            split[0] = split[0].lower()

            if split[0] == 'x-varnish':
                self.logRow['span_id'] = value

            elif split[0] == 'x-varnish-trace':
                self.logRow['trace_id'] = value

            elif split[0] == 'x-varnish-parent':
                self.logRow['parent_id'] = value

            elif split[0] == 'x-varnish-debug':
                self.logRow['debug'] = value

            elif split[0] == 'host':
                ipv4 = value
                port = 0

                if value.find(':') > -1:
                    value = value.split(':')
                    ipv4 = value[0]
                    port = value[1]

                self.logRow['ipv4'] = ipv4
                self.logRow['port'] = port

