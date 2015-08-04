from flask import request, redirect, render_template
from . import index

from .. import db

@index.route('/', methods=['GET'])
def index():
    # read in GET request values
    spanName = request.args.get('spanName')
    serviceName = request.args.get('serviceName')

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

    return render_template('index.html', spans=spans, services=services, spanName=spanName, serviceName=serviceName)
