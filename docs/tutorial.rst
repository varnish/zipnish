==================
Give Zipnish a try
==================

This section aggregates all other chapters in the documentation and will provide a guide
for setting up a working environment with Zipnish.
As a side-note, all steps below have been run on a Centos7 machine.

A fresh Centos7 VM requires the following packages:

    .. code-block:: sh

        $ sudo yum -y install mariadb-devel
        $ sudo yum -y install python-devel
        $ sudo yum -y install python-pip
    

1)  **Start an application server**

    Clone the git repo:

    .. code-block:: sh

        $ git clone https://github.com/varnish/zipnish.git

    
    Start the application server:
    
    .. code-block:: sh
    
        $ cd zipnish/logreader/test
        $ python server.py &
    
    This will spawn a lite web server listening on port ``9999``, the endpoints available in this server
    are as defined in the server.yaml file located in the same folder.

2)  **Install, configure and start Varnish**
    
    Zipnish requires Varnish_ 4, earlier versions are not supported.
    
    .. code-block:: sh
    
        $ sudo yum install -y varnish
    
    Update ``/etc/varnish/default.vcl`` file with the following content:
    
    .. code-block:: sh
    
            vcl 4.0;
    
            # Default backend definition. Set this to point to your content server.
            backend default {
                .host = "127.0.0.1";
                .port = "9999";
            }
    
            sub vcl_recv {
                return(pass);
            }
            
    Start Varnish:

    .. code-block:: sh

        $ sudo service varnish start
        
    Or reload, if Varnish has already been installed:
    
    .. code-block:: sh

        $ sudo service varnish reload
    

    Unless otherwise specified, Varnish will listen on port ``6081.``
    For simplicity reasons ``vcl_recv()`` will pass all requests, refer to the VCL_ section in order to have caching enabled. Notice that the default backend points to the server that has just been spawned previously.
    
.. _VCL: http://zipnish.readthedocs.io/en/latest/vcl.html
.. _Varnish: http://www.varnish-cache.org/
.. _container: https://hub.docker.com/r/mariusm/ubuntu-mariadb/
.. _configuration: http://zipnish.readthedocs.io/en/latest/index.html

3)  **Check that Varnish and the backend are set correctly**
    
    Issue the following request against Varnish:
    
    .. code-block:: sh
    
        $ curl -is http://localhost:6081/api/articles
    
    Expected output:
    
    .. code-block:: sh
    
        127.0.0.1 - - [10/May/2016 11:26:54] "GET /api/auth HTTP/1.1" 200 -
        127.0.0.1 - - [10/May/2016 11:26:54] "GET /api/titles HTTP/1.1" 200 -
        127.0.0.1 - - [10/May/2016 11:26:54] "GET /api/images HTTP/1.1" 200 -
        127.0.0.1 - - [10/May/2016 11:26:55] "GET /api/correct HTTP/1.1" 200 -
        127.0.0.1 - - [10/May/2016 11:26:55] "GET /api/compose HTTP/1.1" 200 -
        127.0.0.1 - - [10/May/2016 11:26:55] "GET /api/articles HTTP/1.1" 200 -
    
        HTTP/1.1 200 OK
        Server: BaseHTTP/0.3 Python/2.7.9
        Date: Tue, 10 May 2016 11:26:55 GMT
        Content-type: text/html
        X-Varnish: 32803
        Age: 0
        Via: 1.1 varnish-v4
        Transfer-Encoding: chunked
        Connection: keep-alive
        Accept-Ranges: bytes
    
4)  **Configure a MariaDb instance**
    
    Install docker:

    .. code-block:: sh
    
        $ sudo yum -y install docker
    
    
    Pull and run the following container_ for setting up a MariaDb instance:
    
    .. code-block:: sh
    
        $ docker pull mariusm/ubuntu-mariadb
        $ docker run -d -p 3306:3306 mariusm/ubuntu-mariadb
    
    Once created, the container will host a mariadb instance with a ``microservice`` database and a user with the following credentials:
    
    **user** = zipnish
    
    **pass** = secret

5)  **Install and configure Zipnish**
    
    Zipnish is available in Pypi, thus run the following command to install it:
    
    .. code-block:: sh
    
        $ pip install -m zipnish
    
    Create a ``/etc/zipnish/zipnish.cfg`` with a content similar as described in configuration_. Retrieve the docker container IP and update the mysql host accordingly in the .cfg file.
    
    Create the log folder:

    .. code-block:: sh
    
        $ sudo mkdir -p /var/log/zipnish
        $ sudo chown -R $(whoami): /var/log/zipnish

    
6)  **Run**
    
    Start the log-reader:
    
    .. code-block:: sh
    
        $ zipnish-logreader &
    
    Start the zipnish UI:
    
    .. code-block:: sh
    
        $ zipnish-ui &
    
    Issue a test request to generate tracking data:
    
    .. code-block:: sh
    
        $ curl -is http://localhost:6081/api/articles
    
7)  **Browse the UI**
    
    Open a browser and navigate to http://127.0.0.1:5000
