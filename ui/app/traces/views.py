from flask import render_template, request, redirect
from . import traces

@traces.route('/<trace_id>', methods=['GET'])
def traces(trace_id):
    return '/trace/%s' % trace_id
