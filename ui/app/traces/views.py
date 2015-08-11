from flask import render_template, request, redirect

from . import traces
from .. import db

from ..utils import ParseTraceURLId


@traces.route('/<hex_trace_id>', methods=['GET'])
def traces(hex_trace_id):
    # hex trace_id converted to long
    traceId = str(ParseTraceURLId(hex_trace_id))

    # get database engine connection
    connection = db.engine.connect()

    # find the number of DISTINCT spans, that above service connects with
    query = "SELECT *  \
            FROM zipkin_annotations \
            WHERE \
            trace_id = %s \
            ORDER BY a_timestamp DESC" \
            % str(traceId)
    resultAnnotations = connection.execute(query)


    return render_template('trace.html')
