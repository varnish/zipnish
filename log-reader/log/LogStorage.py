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
        if row['request_type'] == 'c':
            print 'Client Request, process client start and client recieve'
            print row['timestamp-abs-Start'] + ', ' + row['timestamp-abs-Resp']
        elif row['request_type'] == 'b':
            print 'Backend Request, process client start, server recieve, server send, client recieve'
            print

    def flushSpans(self):
        print self.spans
        self.spans = []

    def flushAnnotations(self):
        print self.annotations
        self.annotations = []
