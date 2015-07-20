#!/usr/bin/env python
import os

from app import create_app

app = create_app(os.getenv('APP_CONFIG') or 'default')

print app

if __name__ == '__main__':
    app.run()
