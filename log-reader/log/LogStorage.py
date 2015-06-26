import time
import pprint

# LogStorage - read and do basic processing of incoming data
class LogStorage:
    def __init__(self):
        self.table = [];
        self.pp = pprint.PrettyPrinter(indent=4)

    def push(self, obj):
        self.pp.pprint(obj)
