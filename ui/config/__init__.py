# we should initialize python package based on envoirnment variable

# load configuration
environ = 'development'

if 'ENV' in os.environ.keys():
    environ = os.environ['ENV']

print 'environ=' + environ


