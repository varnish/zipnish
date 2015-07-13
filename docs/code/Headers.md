| Header  | Description  |
|---|---|
| X-Varnish  |  This header is automatically picked up from the Varnish Shared Memory log. |
| X-Varnish-Parent  | Parent of a request. Each RPC call must have a X-Varnish-Parent. <br/>It is a copy of X-Varnish header at the parent RPC call level. |
| X-Varnish-Trace  |  It is used to connect a Request / RPC call to a trace. Each RPC call except the root RPC call will have a X-Varnish-Trace header. |
| X-Varnish-Debug  |  0 or 1. For now value doesn't signify anything special. It needs to comply with ZipKin, but we'll probably look int this later. |
