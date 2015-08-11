def GenerateTraceURLId(idLong):
    hexStr = ''

    hexStr += format(idLong >> 56 & 0xff, 'x')
    hexStr += format(idLong >> 48 & 0xff, 'x')
    hexStr += format(idLong >> 40 & 0xff, 'x')
    hexStr += format(idLong >> 32 & 0xff, 'x')
    hexStr += format(idLong >> 24 & 0xff, 'x')
    hexStr += format(idLong >> 16 & 0xff, 'x')
    hexStr += format(idLong >>  8 & 0xff, 'x')
    hexStr += format(idLong       & 0xff, 'x')

    return hexStr

def ParseTraceURLId(hexString):
    pass
