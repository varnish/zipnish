========
Examples
========

This section will provide a short example on how to extend an endpoint in order for Zipnish to be aware of it.

Full example code found here:
  https://github.com/varnish/zipnish/blob/master/logreader/test/server.py

Zipnish requires three headers to be available per request basis:

  * X-Varnish           - Request id assigned by Varnish.
  * X-Varnish-Trace     - The id that has been assigned by Varnish to the first incoming request.
  * X-Varnish-Parent    - The id of the parent request which has triggered the current request.

.. code-block:: python

    def do_GET(self):
        x_varnish_header = self.headers['x-varnish']
        trace_header = x_varnish_header

        if 'x-varnish-trace' in self.headers:
            trace_header = self.headers['x-varnish-trace']

        headers = {'x-varnish-trace': trace_header,
                   'x-varnish-parent': x_varnish_header}
    ...

In this specific example there is a very simple web server that handles basic GET requests based on a configuration found in server.yaml:

.. code-block:: yaml

  ---
  traces:
      - trace:
          - url: /api/articles
          - span: /api/auth
          - span: /api/titles
          - span: /api/images
          - span: /api/correct
          - span: /api/compose

The test server is exposed through port 9999, our vcl configuration has a backend the points to this server:

.. code-block:: sh
    
    vcl 4.0;

    backend default {
        .host = "127.0.0.1";
        .port = "9999";
    }

    # For simplicity reason disable caching, see vcl how to's for enabled caching.
    sub vcl_recv {
           return (pass);
    }
    
Given that Varnish has its default settings, the request below:

  $ curl -is http://localhost:6081/api/articles

wil have the following output:

.. code-block:: text

  HTTP/1.1 200 OK
  Server: BaseHTTP/0.3 Python/2.7.9
  Date: Tue, 10 May 2016 08:43:44 GMT
  Content-type: text/html
  X-Varnish: 11
  Age: 0
  Via: 1.1 varnish-v4
  Transfer-Encoding: chunked
  Connection: keep-alive
  Accept-Ranges: bytes

and server output:

.. code-block:: text
  
  127.0.0.1 - - [10/May/2016 08:43:43] "GET /api/auth HTTP/1.1" 200 -
  127.0.0.1 - - [10/May/2016 08:43:43] "GET /api/titles HTTP/1.1" 200 -
  127.0.0.1 - - [10/May/2016 08:43:44] "GET /api/images HTTP/1.1" 200 -
  127.0.0.1 - - [10/May/2016 08:43:44] "GET /api/correct HTTP/1.1" 200 -
  127.0.0.1 - - [10/May/2016 08:43:44] "GET /api/compose HTTP/1.1" 200 -
  127.0.0.1 - - [10/May/2016 08:43:44] "GET /api/articles HTTP/1.1" 200 -
  
The scenario is as follows:

  1. A client does a request to the test server asking for **/articles**
  2. In order to serve **/articles**, subsequent calls are required to other endpoints such as **/auth**, **/titles** ...etc
     For demo purposes these subsequent calls are handled by the same server, what is important to notice is that all sub-requests go through Varnish as well.
     A random sleep time has been added for each request in order to simulate some "hard work".
  3. Zipnish-logreader picks up its required data from Varnishlog as these requests go through.
  4. As data gets written into the MySql database, Zipnish-UI will be able to represent how requests have been issued and how much time each of them has taken.
