All RPC services should be access by a proxy Varnish.

***Process.***

* Client makes a request to Varnish.

* Varnish sends request to a RPC service.

* Varnish gets a response and forwards it to the client.
