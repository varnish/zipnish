import time
import copy
from tabulate import tabulate

# LogStorage - read and do basic processing of incoming data
class LogStorage:
    def __init__(self):
        self.spans = []
        self.annotations = []

        self.minNumOfSpanRecordsForFlush = 1
        self.minNumOfAnnotationRecordsForFlush = 1

    def push(self, row):

        # will result in one or more rows based on timestamp values and requestType
        processedRows = self.preProcess(row)

        if len(self.spans) >= self.minNumOfRecordsForFlush or len(self.annotations) >= self.minNumOfAnnotationRecordsForFlush:
            self.flush()

    def preProcess(self, row):
        # preprocess row data
        if row['request_type'] == 'c':
            print 'Client Request, process client start and client recieve'
            print row['timestamp-abs-Start'] + ', ' + row['timestamp-abs-Resp']
        elif row['request_type'] == 'b':
            print 'Backend Request, process client start, server recieve, server send, client recieve'
            print

    def flush(self):
        print
        print self.rows
        self.rows = []
