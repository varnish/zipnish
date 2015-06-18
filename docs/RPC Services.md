All RPC services should be access by a proxy Varnish.

***Process.***

* Client makes a request to Varnish.

* Varnish sends request to a RPC service.

* Varnish gets a response and forwards it to the client.


***Creating Services***

A generic web-service code is available inside **rpc-services** on root.

Initiate a parent service using Node.js command,

``node app.js --port 5000 --address 127.0.0.1 --service 'Parent'``

--port
--address
--service
