from flask import render_template, request, redirect

from . import traces
from .. import db

from ..utils import ParseTraceURLId


@traces.route('/<hex_trace_id>', methods=['GET'])
def traces(hex_trace_id):
    # hex trace_id converted to long
    traceId = str(ParseTraceURLId(hex_trace_id))

    # find the number of DISTINCT spans, that above service connects with
    query = "SELECT COUNT(DISTINCT span_name) as spanCount, COUNT(DISTINCT service_name) as serviceCount  \
            FROM zipkin_annotations \
            GROUP BY trace_id, span_name, service_name \
            HAVING \
            trace_id = %s \
            ORDER BY a_timestamp DESC" \
            % str(traceId)
    result = connection.execute(query)



    return render_template('trace.html')
