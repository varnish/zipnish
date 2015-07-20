from flask import Flask
from config import config

print config

# create Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return 'Here we come'

if __name__ == '__main__':
    app.run()
