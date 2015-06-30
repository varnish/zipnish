import time
from tabulate import tabulate

# LogStorage - read and do basic processing of incoming data
class LogStorage:
    def __init__(self):
        self.rows = []
        self.minNumOfRecordsForFlush = 1

    def push(self, row):

        # will result in one or more rows based on timestamp values and requestType
        processedRows = self.preProcess(row)

        if len(self.rows) >= self.minNumOfRecordsForFlush:
            self.flush()

    def preProcess(self, row):
        # preprocess row data
        pass

    def flush(self):
        print
        print self.rows
        self.rows = []

