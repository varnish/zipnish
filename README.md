# Tracking Micro-services via Varnish Cache #

## Scope ##

Track timing of micro-service requests by passing micro-service requests through a varnish server.



## Varnish Log Script ##

For now the script merely checks and prints varnish log headers (key: value pairs).

Running the varnish logger script.

> &gt; cd log-reader

> &gt; python sample_varnishlog.py

## UI and Log Storage ##

[zipkin](https://github.com/twitter/zipkin) would be used for backend services and UI. It remains to be seen how it would be connected and used.
