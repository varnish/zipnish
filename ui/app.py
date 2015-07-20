from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Here we come'

if __name__ == '__main__':
    app.run()
