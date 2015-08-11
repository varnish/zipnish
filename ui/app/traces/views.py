from flask import render_template, request, redirect

from . import traces
from .. import db

from ..utils import ParseTraceURLId


@traces.route('/<hex_trace_id>', methods=['GET'])
def traces(hex_trace_id):
    # hex trace_id converted to long
    traceId = str(ParseTraceURLId(hex_trace_id))

    # find the number of DISTINCT spans, that above service connects with
    query = "SELECT COUNT(DISTINCT span_id) as spanCount, parent_id, created_ts, trace_id \
            FROM zipkin_spans \
            GROUP BY trace_id \
            HAVING \
            trace_id IN (%s) \
            ORDER BY created_ts DESC" \
            % str(traceId)
    result = connection.execute(query)



    return render_template('trace.html')
