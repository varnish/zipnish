============
VCL how to's
============

In order for Zipnish to grab its required headers there are a few changes that are required in your VCL. There are two
main scenarios to be handled here:

1. Caching disabled:

.. code-block:: sh
    
    vcl 4.0;

    backend DemoMicroservice {
        .host = "127.0.0.1";
        .port = "9999";
    }

    # disable caching - see further down for another example with caching enabled
    sub vcl_recv {
        if (req.url ~ "^/DemoService") {
           set req.backend_hint = DemoMicroservice;
           return (pass);
        }
    }

2. Caching enabled:

.. code-block:: sh
    
    vcl 4.0;

    backend DemoMicroservice {
        .host = "127.0.0.1";
        .port = "9999";
    }

    # disable caching - see further down for another example with caching enabled
    sub vcl_recv {
        if (req.url ~ "^/DemoService") {
            set req.backend_hint = DemoMicroservice;
        }
    }

    sub vcl_deliver {
        # add the response headers if this is a cache hit
        if (obj.hits > 0) {
            if (req.http.x-varnish-trace) {
                set resp.http.x-varnish-trace = req.http.x-varnish-trace;
            } else {
                set resp.http.x-varnish-trace = req.http.x-varnish;
            }
            set resp.http.x-varnish-parent = req.http.x-varnish;
        }
    }
