import os
from flask import Flask

# create Flask application
app = Flask(__name__)

# load configuration
environ = 'development'

if 'ENV' in os.environ.keys():
    environ = os.environ['ENV']

#print 'environ=' + environ


@app.route('/')
def index():
    return 'Here we come'

if __name__ == '__main__':
    app.run()
