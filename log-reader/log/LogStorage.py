import time
from tabulate import tabulate

# LogStorage - read and do basic processing of incoming data
class LogStorage:
    def __init__(self):
        self.rows = []
        self.minNumOfRecordsForFlush = 5

    def push(self, requestType, row):

        self.rows.append(row)

        if len(self.rows) >= self.minNumOfRecordsForFlush:
            self.flush()

    def flush(self):
        print tabulate(self.rows, self.headers)
        self.rows = []

