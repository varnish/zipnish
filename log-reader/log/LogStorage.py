import time
from tabulate import tabulate

# LogStorage - read and do basic processing of incoming data
class LogStorage:
    def __init__(self):
        self.rows = []
        self.minNumOfRecordsForFlush = 1

    def push(self, row):

        self.rows.append(row)

        if len(self.rows) >= self.minNumOfRecordsForFlush:
            self.flush()

    def flush(self):
        print
        print self.rows
        self.rows = []

