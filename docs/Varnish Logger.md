## Varnish Log Script ##

For now the script merely checks and prints varnish log headers (key: value pairs).

Running the varnish logger script.

> &gt; cd log-reader

> &gt; python reader_varnishlog.py


Essentially the following varnishlog should give us required information needed for ZipKin log.

``varnishlog -i ReqURL,BereqURL,ReqHeader,BereqHeader,RespHeader,BerespHeader,Timestamp``
