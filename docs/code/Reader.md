Reader is responsible for reading Varnish Shared Memory Log.

It reads the following fields.

| Name  | Description  |
|---|---|---|
| VxID  | Unique Varnish Request ID. It is not unique between varnish restarts.  |
| Request Type  | Request can be (client / backend)  |
| Tag  |  e.g. Begin, End, Link, Timestamp, ReqHeader, RespHeader, BereqHeader, BerespHeader |
| Data  | Contains information related to Tag above.  |
