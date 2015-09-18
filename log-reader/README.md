#### Configuring ####

Installing requirements for varnish log reader.

`pip install -r requirements.txt`

*Additional Notes*

If you don't have the mysql dev libraries installed. Please try the following commands.

`sudo apt-get install -y python-dev`

`sudo apt-get install python-mysqldb`


### Database Operations ###

Import mysql database schema. *vmsm* is assumed for database / username / password and host *localhost*.

`mysql -u vmsm -p vmsm < log-reader/schema.sql`

Assign a user to vmsm database.

`CREATE user 'vmsm'@'localhost' IDENTIFIED BY 'vmsm';`