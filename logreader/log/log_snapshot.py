URL_TAGS = ['ReqURL', 'BereqURL']
HEADER_TAGS = ['ReqHeader', 'RespHeader', 'BereqHeader', 'BerespHeader']


class Snapshot(object):

    def __init__(self):
        self.log_snapshot = dict()
        self.callbacks = []

    def add_callback_func(self, func):
        self.callbacks.append(func)

    def fill_snapshot(self, vxid, request_type, tag, data):
        if tag == 'Begin':
            self.log_snapshot.clear()
            self.log_snapshot['begin'] = data
        elif tag == 'End':
            self.log_snapshot['request_type'] = request_type
            self.__on_snapshot_ready()
            self.log_snapshot.clear()

        if tag in URL_TAGS:
            self.log_snapshot['span_name'] = data.rstrip('\x00')
        elif tag == 'Link':
            value = data.split(" ")[1]
            self.log_snapshot['link'] = value
        elif tag == 'Timestamp':
            ts = data.rstrip('\x00').split(" ")
            assert len(ts) == 4

            ts_name_tag = ts[0].rstrip(":")
            ts_abs_tag = "timestamp-%s-%s" % ("abs", ts_name_tag)
            ts_duration_tag = "timestamp-%s-%s" % ("duration", ts_name_tag)
            self.log_snapshot[ts_abs_tag] = ts[1]
            self.log_snapshot[ts_duration_tag] = ts[3]
        elif tag in HEADER_TAGS:
            header_info = data.rstrip('\x00').split(": ")
            header_name = header_info[0].lower()
            header_value = header_info[1].rsplit()[0]

            if header_name == 'x-varnish':
                self.log_snapshot['span_id'] = header_value
            elif header_name == 'x-varnish-trace':
                self.log_snapshot['trace_id'] = header_value
            elif header_name == 'x-varnish-parent':
                self.log_snapshot['parent_id'] = header_value
            elif header_name == 'x-varnish-debug':
                self.log_snapshot['debug'] = header_value
            elif header_name == 'host':
                ipv4 = header_value
                port = 0
                if ":" in header_value:
                    value = header_value.split(":")
                    ipv4 = value[0]
                    port = value[1]

                self.log_snapshot['ipv4'] = ipv4
                self.log_snapshot['port'] = port

    def __on_snapshot_ready(self):
        for func in self.callbacks:
            if func:
                func(self.log_snapshot.copy())
