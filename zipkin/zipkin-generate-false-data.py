import time
import random

def ts_microseconds():
    return int( time.time() * 1000000 )

def generate_id():
    return random.getrandbits(64)

print 'timestamp: ' + str(ts_microseconds())
print 'random id: ' + str(generate_id())
