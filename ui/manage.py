#!/usr/bin/env python
import os

from app import create_app
from flask.ext.script import Shell, Manager

app = create_app(os.getenv('APP_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app)


if __name__ == '__main__':
    manager.run()
