
***DB Schema***

Spans

```
span_id
parent_id
trace_id
span_name
debug
duration
created_ts
```

Annotations

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

Python function to generate timestamp / microsecond

```
import time
int ( time.time() * 1000000 )
```

---

***Process***

1. Start from span table. 
  * Generate 19 digit unique number.
  * Insert that unique number into -> span_id
    * if **parent_id** is available from headers insert it, otherwise leave it NULL
    * if **trace_id** is available from headers insert it, otherwise generate a new trace_id to be used.
      * for now just reuse **span_id** number if **trace_id** is not available and pass it along doing the chain of RPC calls.

