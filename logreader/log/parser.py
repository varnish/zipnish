import socket
import struct


spans = []
annotations = []

CLIENT_RECEIVE = 'cr'
SERVER_RECEIVE = 'sr'
SERVER_SEND = 'ss'


def clear_spans():
    global spans
    del spans[:]


def clear_annotations():
    global annotations
    del annotations[:]


def __ts_convert(row_dict, ts_key, convert_func):
    if ts_key in row_dict:
        ts_value = row_dict[ts_key]
        ts = ts_value if ts_value else ''
        if len(ts):
            row_dict[ts_key] = convert_func(ts)


def __convert_timestamp(timestamp):
    return int(timestamp.replace('.', ''))


def __convert_duration(duration):
    _duration = duration.replace('.', '').lstrip('0')
    return int(_duration) if len(_duration) else 0


def __convert_ip_to_int(ip):
    _ip = socket.gethostbyname(ip)
    return struct.unpack("!I", socket.inet_aton(_ip))[0]


def replace_client_span_id(client_span_id, backend_span_id):
    for span_idx in range(len(spans)):
        span_row = spans[span_idx]

        if span_row['span_id'] == client_span_id:
            if span_row['trace_id'] == span_row['span_id']:
                span_row['trace_id'] = backend_span_id

            span_row['span_id'] = backend_span_id
            spans[span_idx] = span_row


def __parse_client_log(row_dict):
    __ts_convert(row_dict, 'timestamp-abs-Start', __convert_timestamp)
    __ts_convert(row_dict, 'timestamp-duration-Start', __convert_duration)
    __ts_convert(row_dict, 'timestamp-duration-Resp', __convert_duration)
    __ts_convert(row_dict, 'timestamp-abs-Resp', __convert_timestamp)

    if 'trace_id' not in row_dict:
        row_dict['trace_id'] = row_dict['span_id']

    span = {'span_id': row_dict['span_id'],
            'parent_id': row_dict['parent_id'],
            'trace_id': row_dict['trace_id'],
            'span_name': row_dict['span_name'],
            'debug': row_dict['debug'],
            'duration': row_dict['timestamp-duration-Start'],
            'created_ts': row_dict['timestamp-abs-Start']}

    spans.append(span)

    if row_dict['parent_id'] is not None:
        child_span = dict()
        child_span.update(span)
        child_span['duration'] = row_dict['timestamp-duration-Resp']
        child_span['created_ts'] = row_dict['timestamp-abs-Resp']
        spans.append(child_span)


def __parse_backend_log(row_dict):
    __ts_convert(row_dict, 'timestamp-duration-Start', __convert_duration)
    __ts_convert(row_dict, 'timestamp-abs-Start', __convert_timestamp)
    __ts_convert(row_dict, 'timestamp-duration-Bereq', __convert_duration)
    __ts_convert(row_dict, 'timestamp-abs-Bereq', __convert_timestamp)
    __ts_convert(row_dict, 'timestamp-duration-Beresp', __convert_duration)
    __ts_convert(row_dict, 'timestamp-abs-Beresp', __convert_timestamp)
    __ts_convert(row_dict, 'timestamp-duration-BerespBody', __convert_duration)
    __ts_convert(row_dict, 'timestamp-abs-BerespBody', __convert_timestamp)

    if 'trace_id' not in row_dict:
        row_dict['trace_id'] = row_dict['span_id']

    if row_dict['ipv4']:
        row_dict['ipv4'] = __convert_ip_to_int(row_dict['ipv4'])

    begin_tag_data = row_dict['begin'].strip().split(" ")
    client_span_id = begin_tag_data[1]

    replace_client_span_id(client_span_id, row_dict['span_id'])

    annotation = {
        'span_id': row_dict['span_id'],
        'trace_id': row_dict['trace_id'],
        'span_name': row_dict['span_name'],
        'service_name': row_dict['span_name'],
        'value': 'cs',
        'ipv4': row_dict['ipv4'],
        'port': row_dict['port'],
        'a_timestamp': row_dict['timestamp-abs-Start'],
        'duration': row_dict['timestamp-duration-Start']
    }

    client_start_annotation = dict()
    client_start_annotation.update(annotation)
    client_start_annotation['a_timestamp'] = row_dict['timestamp-abs-Bereq']
    client_start_annotation['duration'] = row_dict['timestamp-duration-Bereq']
    client_start_annotation['value'] = SERVER_RECEIVE

    server_rec_annotation = dict()
    server_rec_annotation.update(annotation)
    server_rec_annotation['a_timestamp'] = row_dict['timestamp-abs-Beresp']
    server_rec_annotation['duration'] = row_dict['timestamp-duration-Beresp']
    server_rec_annotation['value'] = SERVER_SEND

    server_resp_annotation = dict()
    server_resp_annotation.update(annotation)
    server_resp_annotation['a_timestamp'] = row_dict[
        'timestamp-abs-BerespBody']
    server_resp_annotation['duration'] = row_dict[
        'timestamp-duration-BerespBody']
    server_resp_annotation['value'] = CLIENT_RECEIVE

    annotations.append(annotation)
    annotations.append(client_start_annotation)
    annotations.append(server_rec_annotation)
    annotations.append(server_resp_annotation)


def parse_log_row(row_dict):
    if 'debug' not in row_dict:
        row_dict['debug'] = 0

    if 'parent_id' not in row_dict:
        row_dict['parent_id'] = 0

    req_type = row_dict['request_type']

    if req_type == 'c':
        __parse_client_log(row_dict)
    elif req_type == 'b':
        __parse_backend_log(row_dict)
