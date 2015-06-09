from flask import Flask

app = Flask(__name__)

# todo
# finish log with log.Fini() call when application crashes / finishes

@app.route('/')
def index():
    return 'UI for varnish log goes in here'

if __name__ == '__main__':
    app.run(debug=True)
