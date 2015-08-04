import json

from time import time
from urllib import unquote
from flask import request, redirect, render_template

from . import index
from .. import db

@index.route('/', methods=['GET'])
def index():
    # read GET values
    spanName = request.args.get('spanName')
    serviceName = request.args.get('serviceName') or unquote(request.cookies.get('last-serviceName'))
    timestamp = request.args.get('timestamp')
    limit = request.args.get('limit') or 10

    formSubmitted = True

    if timestamp is None or timestamp.strip() == '':
        formSubmitted = False
        timestamp = int(time() * 1000000)

    # get database engine connection
    connection = db.engine.connect()

    # query results
    queryResults = None

    # query database based on query parameters if service is given
    if formSubmitted:
        # query results that would be sent over to view
        queryResults = []

        # find all traces to which related to this service
        query = "SELECT DISTINCT trace_id \
                FROM zipkin_annotations \
                WHERE service_name = '%s'" % (serviceName)

        traceIds = []
        resultTraceIds = connection.execute(query)

        for row in resultTraceIds:
            traceIds.append(row['trace_id'])

        if len(traceIds) > 0:
            # find the number of DISTINCT spans, that above service connects with
            query = "SELECT COUNT(DISTINCT span_id) as numSpans \
                    FROM zipkin_spans \
                    WHERE \
                    trace_id IN (%s)" % (",".join(str(traceId) for traceId in traceIds))
            result = connection.execute(query)

            for row in result:
                numSpans = row['numSpans']

        return str(numSpans)

    # populate services
    services = []
    result = connection.execute("SELECT DISTINCT service_name FROM zipkin_annotations")

    for row in result:
        services.append( row['service_name'] )

    spans = []

    if serviceName:
        query = "SELECT DISTINCT span_name FROM zipkin_annotations WHERE service_name='%s'" % serviceName
        result = connection.execute(query)

        for row in result:
            spans.append( row['span_name'] )

    if len(spans) > 0:
        spans.insert(0, 'all')

    # close connection
    connection.close()

    return render_template('index.html', \
            results=queryResults, \
            services=services, spans=spans, \
            get_SpanName=spanName, get_ServiceName=serviceName, \
            get_Timestamp=timestamp, get_Limit=limit)
