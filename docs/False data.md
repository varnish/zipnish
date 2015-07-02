False data document although irrelevant as of now.
But it remains here for understandability reason, for example, if one 
might want to extract certain code snippets e.g. generating timestamps
etc.

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
     * for now just reuse **span_id** number if **trace_id** is not available and pass it along the chain of RPC calls.
  * created_ts will be 16-digit timestamp generated with above python script.
  * duration will remain NULL for now.
    * It needs to be calculated when ``value = cr`` for ``trace_id = span_id``
2. Use ``span_id, trace_id`` generated in **1.** to populate annotations table.
 * service_name (use example_service as a name just for example sake)
 * value (restrict yourself to these four values cs / sr / ss / cr, other value how they can be used need to be understood as used in example, but it comes later.)
  * cs = client send, sr = server recieve, ss = server send, cr = client recieve

***Rough***

* create functions to: generate microsecond timestamp, generate random id
* get a handle to database connection
* create function add_span
* create function add_span_annotation

***Notes***

For now randomness is generated using random.getrandombits(64). Skipping the idea of using microseconds() as id for ```trace_id, span_id``` etc.

In future if need following hash can be used, credits :point_down:

sha256(varnish host IP, XID, timestamp) :clap: @espebra :clap:

All root spans which start a trace.
``SELECT * FROM zipkin_spans WHERE span_id IN (SELECT span_id FROM `zipkin_spans` WHERE `parent_id` IS NULL ORDER BY `parent_id` ASC)``


***Additional Packages***

Install Python MySQL using the following command below,

```
sudo apt-get install -y python-mysqldb
sudo apt-get install -y libmysqlclient-dev
pip install mysql
```

***Assumptions***

* Spans contains RPC calls. Each new span without a parent starts a trace.
  * Span which starts a trace occurs only once inside zip_spans. It's first entry is marked by **sr** server recieve event.
* Each RPC call has events such as, 
  * **cs** - client send is marked by a first entry inside zipkin_spans
  * **sr** - server recieve is marked by a second entry inside zipkin_spans
