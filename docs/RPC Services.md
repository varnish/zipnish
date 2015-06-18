All RPC services should be access by a proxy Varnish.

***Process.***

* Client makes a request to Varnish.

* Varnish sends request to a RPC service.

* Varnish gets a response and forwards it to the client.


***Creating Services***

```node app.js --port 5000 --address 127.0.0.1 --service 'Parent'``
