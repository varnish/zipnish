======
Docker
======

Unless you have a MySql instance at hand, this ubuntu based image will spawn a mariadb instance. This db instance will be the one used by both the logreader and the ui. Check the ip of your docker setup and update the zipnish.cfg accordingly.

This image relies on two extra files: **database.sql** and **init-db.sh**. Both these files are available in the /docker folder within the zipnish source code. The two extra files are responsible for the creation and initialisation of an user and db tables that Zipnish will use further down the line. Browse to this folder and run the following commands:

.. code-block:: sh

  $ docker pull mariusm/ubuntu-mariadb
  $ docker run -d -p 3306:3306 mariusm/ubuntu-mariadb


A database and db user with the following credentials will be available, if you're going to use this db instance, make sure that zipnish.cfg reflects these settings:

  **user** = zipnish
  
  **pass** = secret
  
  **db_name** = microservice


To quickly check that the db instance is up and running, you could connect to it directly with a mysql client.
Retrieve the ip of your docker setup and connect to the mariadb instance as follows:

.. code-block:: sh

  $ mysql -u zipnish -h "your docker ip" --paswword=secret
  
On a MacOs machine you can simply run the following command:

.. code-block:: sh

  $ mysql -u zipnish -h $(boot2docker ip) --password=secret
