#!/usr/bin/env python
import os

from app import create_app, db

# configuration file path
config_path = os.path.dirname(os.path.abspath(__file__)) + '/ui.cfg'

app = create_app(config_path)

if __name__ == '__main__':
    app.run(host=app.config['HOST'], 
    		port=app.config['PORT'], 
    		debug=app.config['DEBUG'])