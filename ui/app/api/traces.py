from flask import render_template, request, redirect
from . import api

@api.route('/trace/<trace_id>')
def trace(trace_id):
    return '/trace/%s' % trace_id
