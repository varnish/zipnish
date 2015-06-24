By default varnishlog is grouped by Vxid

* X-Varnish same as RequestID

Vxid is unique therefore,

(ZipKin field) span_id = Vxid (Varnish Header)

***Timestamps***

**Request**



**Backend Request**

| ZipKin Annotation | varnishlog Header  |
|---|---|
| (sr) server recieve   | Bereq (Backend request)  |
| (ss) server send   | Beresp (Backend response)  |
