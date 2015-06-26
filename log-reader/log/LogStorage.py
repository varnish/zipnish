import time
from tabulate import tabulate

# LogStorage - read and do basic processing of incoming data
class LogStorage:
    def __init__(self):
        self.rows = []
        self.minNumOfRecordsForFlush = 5

    def push(self, requestType, obj):

        self.rows.append([ obj['BereqURL'] ])

        if len(self.rows) > self.minNumOfRecordsForFlush:
            self.flush()

    def flush(self):
        print tabulate(self.rows, ['BereqURL'])
        self.rows = []

