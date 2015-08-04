from time import time
from flask import request, redirect, render_template

from . import index
from .. import db

@index.route('/', methods=['GET'])
def index():
    # read GET values
    spanName = request.args.get('spanName')
    serviceName = request.args.get('serviceName')
    timestamp = request.args.get('timestamp')
    limit = request.args.get('limit')

    if timestamp is None or timestamp.strip() == '':
        timestamp = int(time() * 1000000)

    # get database engine connection
    connection = db.engine.connect()

    # populate spans
    spans = []
    result = connection.execute("SELECT DISTINCT span_name FROM zipkin_spans")

    for row in result:
        spans.append( row['span_name'] )

    # populate services
    services = []
    result = connection.execute("SELECT DISTINCT service_name FROM zipkin_annotations")

    for row in result:
        services.append( row['service_name'] )

    # close connection
    connection.close()

    return render_template('index.html', \
            spans=spans, services=services, \
            get_SpanName=spanName, get_ServiceName=serviceName, \
            get_Timestamp=timestamp, get_Limit=limit)
