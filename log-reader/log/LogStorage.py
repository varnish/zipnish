import time
from tabulate import tabulate

# LogStorage - read and do basic processing of incoming data
class LogStorage:
    def __init__(self):
        self.rows = []
        self.headers = ['URL']
        self.minNumOfRecordsForFlush = 5

    def push(self, requestType, obj):

        if requestType == 'c':
            self.rows.append([ obj['ReqURL'] ])
        elif requestType == 'b':
            self.rows.append([ obj['BereqURL'] ])

        if len(self.rows) > self.minNumOfRecordsForFlush:
            self.flush()

    def flush(self):
        print tabulate(self.rows, self.headers)
        self.rows = []

