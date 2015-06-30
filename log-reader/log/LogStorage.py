import time
import copy
from tabulate import tabulate

# LogStorage - read and do basic processing of incoming data
class LogStorage:
    def __init__(self):
        self.spans = []
        self.annotations = []

        self.minNumOfSpansToFlush = 2
        self.minNumOfAnnotationsToFlush = 4

    def push(self, row):
        # process row to attach data to span / annotation
        self.process(row)

        if len(self.spans) >= self.minNumOfSpansToFlush:
            self.flushSpans()

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
            row['timestamp-duration-Start'] = self.convertDuration(row['timestamp-duration-Start'])
            row['timestamp-abs-Start'] = self.convertTimestamp(row['timestamp-abs-Start'])
            row['timestamp-duration-Resp'] = self.convertDuration(row['timestamp-duration-Resp'])
            row['timestamp-abs-Resp'] = self.convertTimestamp(row['timestamp-abs-Resp'])

            span = {\
                'span_id': row['span_id'], \
                'parent_id': row['parent_id'], \
                'trace_id': row['trace_id'], \
                'span_name': row['span_name'], \
                'debug': row['debug'], \
                'duration': row['timestamp-duration-Start'], \
                'created_ts': row['timestamp-abs-Start']
            }

            # Server Recieve
            self.spans.append( copy.copy(span) )

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

            annotation = {\
                'span_id': row['span_id'], \
                'trace_id': row['trace_id'], \
                'span_name': row['span_name'], \
                'service_name': '', \
                'value': 'cs', \
                'ipv4': row['ipv4'], \
                'port': row['port'], \
                'a_timestamp': row['timestamp-abs-Start'], \
                'duration': row['timestamp-duration-Start']
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

    def convertTimestamp(self, timestamp):
        # probably varnish GMT-0, need to confirm it later
        return int(float(timestamp))

    def convertDuration(self, duration):
        # this one is the most important value, below conversion gives us
        # value in seconds, milliseconds through would be better
        return int(float(duration))

    def flushSpans(self):
        self.printTable(self.spans)
        self.spans = []

    def flushAnnotations(self):
        self.printTable(self.annotations)
        self.annotations = []

    def printTable(self, rows):
        output = {\
                    'span_id': [], \
                    'trace_id': [], \
                    'span_name': [], \
                    'duration': [] \
                }

        if 'a_timestamp' in rows[0]:
            #output['service_name'] = []
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

        print tabulate(output, output.keys(), tablefmt="fancy_grid")
        print


