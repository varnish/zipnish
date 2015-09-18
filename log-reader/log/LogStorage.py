import time
import copy

# tabulate, collections used for visual printing data validation
from collections import OrderedDict
from tabulate import tabulate

# LogStorage - read and do basic processing of incoming data
class LogStorage:
    def __init__(self, db):
        # connection to database
        self.db = db

        # Database spans
        self.spans = []

        # database annotations
        self.annotations = []

        # minimum number of span data points before flushing data to database
        self.minNumOfSpansToFlush = 2

        # minimum number of annotation data points before flushing data to database
        self.minNumOfAnnotationsToFlush = 4

    def push(self, row):
        # process row to attach data to span / annotation
        self.process(row)

        if len(self.annotations) >= self.minNumOfAnnotationsToFlush:
            self.flushAnnotations()

    def process(self, row):
        # process row data

        if 'debug' not in row:
            row['debug'] = 0

        if 'parent_id' not in row:
            row['parent_id'] = 0

        if row['request_type'] == 'c':

            # client request considered for span
            row['timestamp-abs-Start'] = self.convertTimestamp(row['timestamp-abs-Start'])
            row['timestamp-duration-Start'] = self.convertDuration(row['timestamp-duration-Start'])

            row['timestamp-duration-Resp'] = self.convertDuration(row['timestamp-duration-Resp'])
            row['timestamp-abs-Resp'] = self.convertTimestamp(row['timestamp-abs-Resp'])

            # add backend request link as key, add reference to client request

            if 'trace_id' not in row:
                row['trace_id'] = row['span_id']

            # TODO: this needs to be looked into further, this check needs to be documented
            # and elaborated upon why we have done this
            # probably because parent the top most span, which starts the trace
            # needs to have it's varnish VxID come from the backend request, and not from the 
            # client request

            span = {\
                'span_id': row['span_id'], \
                'parent_id': row['parent_id'], \
                'trace_id': row['trace_id'], \
                'span_name': row['span_name'], \
                'debug': row['debug'], \
                'duration': row['timestamp-duration-Start'], \
                'created_ts': row['timestamp-abs-Start'] \
            }

            # Server Recieve
            self.spans.append( copy.copy(span) )

            #print "CLIENT -> " + row['span_name'] + ("; span_id: " + str(row['span_id']) + "; parent_id: " + str(row['parent_id']))

            if row['parent_id'] is not None:
                span['duration'] = row['timestamp-duration-Resp']
                span['created_ts'] = row['timestamp-abs-Resp']

                # Server Response
                self.spans.append( span )

        elif row['request_type'] == 'b':

            # backend request considered for annotations
            row['timestamp-duration-Start'] = self.convertDuration(row['timestamp-duration-Start'])
            row['timestamp-abs-Start'] = self.convertTimestamp(row['timestamp-abs-Start'])
            row['timestamp-duration-Bereq'] = self.convertDuration(row['timestamp-duration-Bereq'])
            row['timestamp-abs-Bereq'] = self.convertTimestamp(row['timestamp-abs-Bereq'])
            row['timestamp-duration-Beresp'] = self.convertDuration(row['timestamp-duration-Beresp'])
            row['timestamp-abs-Beresp'] = self.convertTimestamp(row['timestamp-abs-Beresp'])
            row['timestamp-duration-BerespBody'] = self.convertDuration(row['timestamp-duration-BerespBody'])
            row['timestamp-abs-BerespBody'] = self.convertTimestamp(row['timestamp-abs-BerespBody'])

            if 'trace_id' not in row:
                row['trace_id'] = row['span_id']

            if row['ipv4'] is not None:
                row['ipv4'] = self.convertIP2Integer(row['ipv4'])

            indexLeft = row['begin'].index(' ') + 1
            indexRight = row['begin'].index(' ', indexLeft)
            clientSpanId = row['begin'][indexLeft:indexRight]

            # print "Before: " + str(self.spans)
            # print "replace client span id -> " + clientSpanId + " WITH " + row["span_id"]
            self.replaceClientSpanId(clientSpanId, row['span_id'])
            # print "After: "  + str(self.spans)

            if len(self.spans) >= self.minNumOfSpansToFlush:
                self.flushSpans()

            #print "BACKEND -> " + row['span_name'] + ("; span_id: " + str(row['span_id']) + ", parent_id: " + str(row['parent_id']))

            annotation = {\
                'span_id': row['span_id'], \
                'trace_id': row['trace_id'], \
                'span_name': row['span_name'], \
                'service_name': row['span_name'], \
                'value': 'cs', \
                'ipv4': row['ipv4'], \
                'port': row['port'], \
                'a_timestamp': row['timestamp-abs-Start'], \
                'duration': row['timestamp-duration-Start'] \
            }

            # Client Start
            self.annotations.append( copy.copy(annotation) )

            annotation['a_timestamp'] = row['timestamp-abs-Bereq']
            annotation['duration'] = row['timestamp-duration-Bereq']
            annotation['value'] = 'sr'

            # Server Recieve
            self.annotations.append( copy.copy(annotation) )

            annotation['a_timestamp'] = row['timestamp-abs-Beresp']
            annotation['duration'] = row['timestamp-duration-Beresp']
            annotation['value'] = 'ss'

            # Server Response
            self.annotations.append( copy.copy(annotation) )

            annotation['a_timestamp'] = row['timestamp-abs-BerespBody']
            annotation['duration'] = row['timestamp-duration-BerespBody']
            annotation['value'] = 'cr'

            # Client Recieve
            self.annotations.append( copy.copy(annotation) )

    def replaceClientSpanId(self, clientSpanId, backendSpanId):
        for spanIndex in range(len(self.spans)):
            spanRow = self.spans[spanIndex]
            #print "spanRow => " + str(spanRow['span_id']) + " == " + clientSpanId + " > " + str(spanRow['span_id'] == clientSpanId)

            if spanRow['span_id'] == clientSpanId:
                if spanRow['trace_id'] == spanRow['span_id']:
                    spanRow['trace_id'] = backendSpanId

                spanRow['span_id'] = backendSpanId
                self.spans[spanIndex] = spanRow

    def convertIP2Integer(self, ip):
        parts = ip.split('.')
        return (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])

    def convertTimestamp(self, timestamp):
        # probably varnish GMT-0, need to confirm it later
        return int(timestamp.replace('.', ''))
        #return int(float(timestamp)) * 1000000

    def convertDuration(self, duration):
        # this one is the most important value, below conversion gives us
        # value in seconds, milliseconds through would be better
        duration = duration.replace('.', '').lstrip('0')

        if len(duration) > 0:
            duration = int(duration)
        else:
            duration = 0
        return duration

    def flushSpans(self):
        print "flushing spans"
        #self.printTable(self.spans)
        self.db.insert('spans', self.spans)
        self.spans = []

    def flushAnnotations(self):
        #self.printTable(self.annotations)
        self.db.insert('annotations', self.annotations)
        self.annotations = []

    def printTable(self, rows):
        output = {\
                    'span_id': [], \
                    'trace_id': [], \
                    'span_name': [], \
                    'duration': [] \
                }

        if 'a_timestamp' in rows[0]:
            output['service_name'] = []
            output['value'] = []
            output['ipv4'] = []
            output['port'] = []
            output['a_timestamp'] = []
        else:
            output['parent_id'] = []
            output['debug'] = []
            output['created_ts'] = []

        for dictionary in rows:
            for key, value in dictionary.iteritems():
                if key in output:
                    output[ key ].append( value )

        headers = sorted(output.keys())
        orderedDictionary = OrderedDict(sorted(output.items()))

        print tabulate(orderedDictionary, headers, tablefmt="fancy_grid")
        print


