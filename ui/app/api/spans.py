from flask import render_template, request, redirect
from . import api

@api.route('/spans')
def spans():
    return '/spans'
