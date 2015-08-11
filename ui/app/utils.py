import sys

def GenerateTraceURLId(idLong):
    return hex(idLong)

def ParseTraceURLId(hexString):
    return long(hexString, 16)
