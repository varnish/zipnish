from flask import render_template, request, redirect
from . import traces
from ..utils import ParseTraceURLId

@traces.route('/<trace_id>', methods=['GET'])
def traces(trace_id):
    return str(ParseTraceURLId(trace_id))
    return render_template('trace.html')
