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
