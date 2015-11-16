from flask import render_template, request, redirect

from . import traces
from .. import db

import sys

from ..utils import ParseTraceURLId, findTraceDepth, generateTraceTimeMarkers


@traces.route('/<hex_trace_id>', methods=['GET'])
def traces(hex_trace_id):
    # hex trace_id converted to long
    traceId = str(ParseTraceURLId(hex_trace_id))

    # get database engine connection
    connection = db.engine.connect()

    # find trace information
    query = "SELECT *  \
            FROM zipnish_annotations \
            WHERE \
            trace_id = %s \
            ORDER BY a_timestamp ASC, service_name ASC" \
            % str(traceId)
    resultAnnotations = connection.execute(query)

    minTimestamp = sys.maxint
    maxTimestamp = 0

    span_ids = []
    service_names = []

    spans = {}

    for row in resultAnnotations:
        span_id = row['span_id']
        trace_id = row['trace_id']
        span_name = row['span_name']
        service_name = row['service_name']
        value = row['value']
        ipv4 = row['ipv4']
        port = row['port']
        a_timestamp = row['a_timestamp']

        minTimestamp = min(a_timestamp, minTimestamp)
        maxTimestamp = max(a_timestamp, maxTimestamp)

        if span_id not in span_ids:
            span_ids.append(span_id)
            spans[span_id] = {}

        if service_name not in service_names:
            service_names.append(service_name)

        spans[span_id]['spanId'] = span_id
        spans[span_id]['serviceName'] = service_name
        spans[span_id]['spanName'] = span_name

    totalDuration = (maxTimestamp - minTimestamp) / 1000
    totalSpans = len(span_ids)
    totalServices = len(service_names)

    #return str(spans)

    # find depth information
    query = "SELECT DISTINCT span_id, parent_id \
            FROM zipnish_spans \
            WHERE trace_id = %s" % traceId
    depthResults = connection.execute(query)

    depthRows = {}
    for row in depthResults:
        depthRows[row['span_id']] = row['parent_id']

    totalDepth = findTraceDepth(depthRows)

    # fetch all annotations related to this trace
    query = "SELECT span_id, span_name, service_name, \
            value, ipv4, port, a_timestamp \
            FROM `zipnish_annotations` \
            WHERE trace_id = %s" % traceId
    allAnnotations = connection.execute(query)

    annotations = []
    for row in allAnnotations:
        annotations.append( row )

    # generate time markers
    timeMarkers = generateTraceTimeMarkers(totalDuration)

    return render_template('trace.html', \
            spanParentDict=depthRows,
            annotations=annotations,
            totalDuration=totalDuration, \
            totalSpans=totalSpans, \
            totalServices=totalServices, \
            totalDepth=totalDepth, \
            timeMarkers=timeMarkers, \
            spans=spans)
