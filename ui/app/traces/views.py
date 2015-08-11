from flask import render_template, request, redirect
from . import traces

@traces.route('/<trace_id>', methods=['GET'])
def traces(trace_id):
    return trace_id
    return render_template('trace.html')
