from flask import render_template, request, redirect
from . import api

@api.route('/dependencies')
def query():
    return '/dependencies'
