By default varnishlog is grouped by Vxid.

X-Varnish same as RequestID. Therefore Vxid is unique and can be used as an identifier for trace_id or span_id.



| ZipKin Field | varnishlog Header  |
|---|---|
| span_id   | Vxid (varnish request id)  |


***Timestamps***

**Request**

| ZipKin Annotation | varnishlog Header  |
|---|---|
| cs - client start   | Start (client start)  |
| cr - client recieve   | Resp (client recieve)  |

**Backend Request**

| ZipKin Annotation | varnishlog Header  |
|---|---|
| sr - server recieve   | Bereq (backend request)  |
| ss - server send   | Beresp (backend response)  |


Can't find parent_id or any kind of reference (X-Forwarded / X-Reference) to connect one request with an parent request.

Therefore we keep ``parent_id = NULL`` for now.

We will reuse Vxid inside ``trace_id`` as well. Which will make ``trace_id`` same as ``span_id``. Trace and Span identifiers can be the same as per [ZipKin documentation](http://twitter.github.io/zipkin/Instrumenting.html).

>**Trace Id**
>
>The overall ID of the trace. Every span in a trace will share this ID.
>
>**Span Id**
>
>The ID for a particular span. This may or may not be the same as the trace id.
