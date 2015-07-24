from flask import request, redirect, render_template
from . import index

@index.route('/')
def index():
    return '/'
