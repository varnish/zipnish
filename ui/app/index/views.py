import sys
import string
import json
import time

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
        timestamp = int(time.time() * 1000000)

    # get database engine connection
    connection = db.engine.connect()

    # query results
    traceResults = None

    # query database based on query parameters if service is given
    if formSubmitted:
        # query results that would be sent over to view
        traceResults = []

        # find all traces to which related to this service
        query = "SELECT DISTINCT trace_id \
                FROM zipkin_annotations \
                WHERE service_name = '%s'"

        # order by
        query += " ORDER BY a_timestamp DESC"

        # limit search results
        query += " LIMIT 0, %s"

        # format search results
        query = query % (serviceName, limit)

        traceIds = []
        resultTraceIds = connection.execute(query)

        for row in resultTraceIds:
            traceIds.append(row['trace_id'])

        if len(traceIds) > 0:
            # find the number of DISTINCT spans, that above service connects with
            query = "SELECT COUNT(DISTINCT span_id) as spanCount, parent_id, created_ts, trace_id \
                    FROM zipkin_spans \
                    GROUP BY trace_id \
                    HAVING \
                    trace_id IN (%s) \
                    ORDER BY created_ts DESC" \
                    % (",".join(str(traceId) for traceId in traceIds))
            result = connection.execute(query)

            for row in result:
                trace = {}

                trace['serviceName'] = serviceName
                trace['spanCount'] = row['spanCount']
                trace['trace_id'] = row['trace_id']

                startTime = (int(row['created_ts']) / 1000000)
                trace['startTime'] = time.strftime('%m-%d-%YT%H:%M:%S%z', time.gmtime(startTime))

                servicesQuery = "SELECT service_name, `value`, a_timestamp \
                        FROM zipkin_annotations \
                        WHERE trace_id = %s AND \
                        `value` IN ('cs', 'sr', 'ss', 'cr') \
                        ORDER BY service_name ASC" % (row['trace_id'])
                servicesResult = connection.execute(servicesQuery)

                services = {}
                service = None

                for serviceRow in servicesResult:
                    if serviceRow['service_name'] not in services:
                        services[serviceRow['service_name']] = {}
                        service = services[serviceRow['service_name']]

                    service[serviceRow['value']] = serviceRow['a_timestamp']

                duration = 0
                serviceDuration = 0
                serviceDurations = []

                minTimestamp = sys.maxint
                maxTimestamp = 0

                selectedServiceDuration = 0

                for key in services:
                    service = services[key]
                    if 'cs' in service:
                        minTimestamp = min(service['cr'], minTimestamp)
                        maxTimestamp = max(service['cs'], maxTimestamp)

                        serviceDuration = service['cr'] - service['cs']
                    else:
                        minTimestamp = min(service['sr'], minTimestamp)
                        maxTimestamp = max(service['ss'], maxTimestamp)

                        serviceDuration = service['ss'] - service['sr']

                    if serviceName == key:
                        selectedServiceDuration = serviceDuration

                    # service duration
                    serviceDurations.append({
                            'name': key,
                            'duration': serviceDuration
                        })

                    # adding up duration to get total duration time
                    duration = duration + serviceDuration

                # total duration for a trace
                trace['duration'] = duration

                # service durations

                # sort service durations
                serviceDurations = sorted(serviceDurations, key=lambda x: x['name'])

                trace['serviceDurations'] = serviceDurations

                #trace['serviceTimestampMin'] = minTimestamp
                #trace['serviceTimestampMax'] = maxTimestamp

                servicesTotalDuration = (maxTimestamp - minTimestamp) / 1000
                trace['servicesTotalDuration'] = '{:.3f}'.format(servicesTotalDuration)

                selectedServicePercentage = int(((selectedServiceDuration / servicesTotalDuration) * 100) / 1000)
                trace['selectedServicePercentage'] = selectedServicePercentage

                traceResults.append( trace )

        #return json.dumps(traceResults)

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
            results=traceResults, \
            services=services, spans=spans, \
            get_SpanName=spanName, get_ServiceName=serviceName, \
            get_Timestamp=timestamp, get_Limit=limit)
