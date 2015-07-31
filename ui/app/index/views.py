from flask import request, redirect, render_template
from . import index

from .. import db

@index.route('/', methods=['GET'])
def index():
    connection = db.engine.connect()
    result = connection.execute("SELECT DISTINCT span_name FROM zipkin_spans")

    spans = []
    for row in result:
        spans.append( row['span_name'] )

    connection.close()

    return render_template('index.html', spans=spans)
