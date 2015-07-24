from flask import render_template, request, redirect
from . import api

@api.route('/query')
def query():
    return '/query'
