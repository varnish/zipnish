from flask import Flask

# create Flask application
app = Flask(__name__)

# basic configuration settings
app.config['DEBUG'] = True


@app.route('/')
def index():
    return 'Here we come'

if __name__ == '__main__':
    app.run()
