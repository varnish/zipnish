#!/usr/bin/env python
import os

from app import create_app
from flask.ext.script import Manager

app = create_app(os.getenv('APP_CONFIG') or 'default')
manager = Manager(app)

print manager

if __name__ == '__main__':
    app.run()
