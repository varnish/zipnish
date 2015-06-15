
db schema

spans

```
span_id
parent_id
trace_id
span_name
debug
duration
created_ts
```

annotations

```
span_id
trace_id
span_name
service_name
value
ipv4
port
a_timestamp
duration
```
All timestamps are in micro-seconds. Durations (difference between timestamps) are also in micro-seconds.
