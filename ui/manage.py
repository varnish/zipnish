#!/usr/bin/env python
import os

from app import create_app, db
from flask.ext.script import Shell, Manager

# configuration file path
config_path = os.path.dirname(os.path.abspath(__file__)) + '/ui.cfg'

app = create_app(config_path)
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db)

# python manage.py shell
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()