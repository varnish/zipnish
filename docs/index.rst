=======
Zipnish
=======

Microservice monitoring tool based on Varnish Cache. Currently it only supports Varnish 4.

Installation
============

Install with pip::

    $ python -m pip install zipnish

Configuration
=============

A configuration file found at **/etc/zipnish/zipnish.cfg** is required with the following content:

.. code-block:: sh

    [Database]
    # Db settings for the MySql connection.

    # MySql host
    host = 192.168.59.103

    # Database name
    db_name = microservice

    # User name
    user = some_user

    # Password
    pass = secret

    # Connection keep-alive
    keep_alive = true

    [Cache]
    # Defines which cache to fetch logs from.
    # Name of the cache (same value sent via the -n argument)
    # name = demo

    [Log]
    # Path to the daemon logfile.
    log_file = /var/log/zipnish/zipnish.log

    # Valid log_levels are: DEBUG, INFO, WARNING, ERROR
    log_level = DEBUG


Contents:


.. toctree::
   :maxdepth: 1

   ui
   vcl
   docker
   examples
   changes
