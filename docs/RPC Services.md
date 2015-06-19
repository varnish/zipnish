All RPC services should be access by a proxy Varnish.

***Broad Overview***

* Client makes a request to Varnish.

* Varnish sends request to a RPC service.

* Varnish gets a response and forwards it to the client.


***Installing Node.js***

Installing instructions for node.js can be found on
[https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager)

In short, running below on debian as root will setup Node.js

``apt-get install -y nodejs``
``curl -sL https://deb.nodesource.com/setup_0.12 | sudo bash -``


***Configuring Services***

Changing directory to ``rpc-service`` and running ``npm install`` should setup everything.

Try the following commands on your command line / bash.

```
> cd rpc-service
> npm install
```

***Creating Services***

A generic web-service code is available inside ``rpc-service`` on root.

Initiate a parent service using Node.js command,

``node app.js --port 5000 --address 127.0.0.1 --service 'Parent'``

***Command line parameters***

| Name        | Value           | Status    | Example |
| ------------- |-------------| -----|-----|----|
| port      | integer > 0 | required | --port 5000 |
| address      | ip-address / domain name to a web-service      |   required | --address 127.0.0.1 |
| service | A string to specify service name to run.      |    required |  --service 'Fetch News' |
| call | repeat argument to make call to multiple RPC-services in parallel. This can be url to an external service as well, just think of it as specifying a URL for web-service. e.g.      |     | --call 127.0.0.1:5001/ |
| flow | parallel / series | required, if multiple ``call`` arguments passed | --flow parallel |
