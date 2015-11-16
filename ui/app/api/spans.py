import json

from flask import render_template, request, redirect, make_response

from . import api
from .. import db

@api.route('/spans', methods=['GET'])
def spans():
    # read GET values
    serviceName = request.args.get('serviceName')

    # get database engine connection
    connection = db.engine.connect()

    # query for results
    spans = []
    spansQuery = "SELECT DISTINCT span_name \
            FROM zipnish_annotations \
            WHERE service_name='%s'" % serviceName

    result = connection.execute(spansQuery)

    for row in result:
        spans.append( row['span_name'] )

    return json.dumps(spans)
