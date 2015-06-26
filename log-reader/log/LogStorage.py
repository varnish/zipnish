import time

# LogStorage - read and do basic processing of incoming data
class LogStorage:
    def __init__(self):
        self.table = [];

    def push(self, obj):
        print obj
