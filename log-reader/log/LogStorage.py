import time
import copy
from tabulate import tabulate

# LogStorage - read and do basic processing of incoming data
class LogStorage:
    def __init__(self):
        self.spans = []
        self.annotations = []

        self.minNumOfSpansToFlush = 1
        self.minNumOfAnnotationsToFlush = 1

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
            # client request considered for, span processing
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

            self.spans.append( copy.copy(span) )

            span['duration'] = row['timestamp-duration-Resp']
            span['created_ts'] = row['timestamp-abs-Resp']

            self.spans.append( span )

        elif row['request_type'] == 'b':
            print 'Backend Request, process client start, server recieve, server send, client recieve'
            print

    def convertTimestamp(self, timestamp):
        return timestamp.replace('.', '')

    def convertDuration(self, duration):
        duration = duration.replace('.', '').lstrip('0')

        if len(duration) == 0:
            duration = 0

        return duration

    def flushSpans(self):
        print self.spans
        self.spans = []

    def flushAnnotations(self):
        print self.annotations
        self.annotations = []
