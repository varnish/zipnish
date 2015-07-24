from flask import render_template, request, redirect
from . import api

@api.route('/pin/query')
def query(pin_id):
    return '/pin/query'
