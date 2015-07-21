####User interface for log reader.####


#####Solution Process#####

1. Mimic API calls for ZipKin inside Flask interface.
2. Run the UI without API calls.
3. Connect each API call one by one with Flask interface.


#####Environment Variables#####

Most of the environment variables specified below are used inside [config.py](config.py)

|  Name 	|  Default 	|  Required 	|  Comments 	|
|---	|---	|:---:	|---	|
| APP_CONFIG  	|  development 	|  no 	|   values: development / testing / production. 	|
| DB_USER  	|   	|  yes 	|  database username 	|
| DB_PASS  	|   	|  yes 	|  database password 	|
| DB_HOST  	|   	|  yes 	|  database host 	|
| DB_PORT  	|   	|  yes 	|  database port 	|
| DB_NAME  	|   	|  yes 	|  database name 	|


#####Application Server#####

Before you run the app, it is required to set some environment variables as listed above.

Envoirnment variables can be temporarily passed to a running webserver as follows,

`$> APP_CONFIG=development DB_USER=zipkin DB_PASS=kinect DB_HOST=127.0.0.1 DB_PORT=3306 DB_NAME=zipkin python manage.py runserver`

Otherwise you need to setup environment variables separately and run the web server using,

`$> python manage.py runserver`


#####Application Shell#####

To run application inside a command line shell using the following.

`$> APP_CONFIG={ENVOIRNMENT_NAME} python manage.py runserver`

With this you will be able to interact with application variables, example: `app`


#####ZipKin/Scala Reference#####

Backend for ZipKin web interface is written using Scala.

It can be found on the following link,

[https://github.com/openzipkin/zipkin/tree/master/zipkin-web/src/main/scala/com/twitter/zipkin/common](https://github.com/openzipkin/zipkin/tree/master/zipkin-web/src/main/scala/com/twitter/zipkin/common)

#####Install bower (if not already installed)#####

[http://bower.io/#install-bower](http://bower.io/#install-bower)

#####Installing Frontend Dependencies#####

`$> cd ui/resources`

`$> bower install`

#####System#####

**[app](app/)** directory contains application. Written in flask.

**[user interface](ui/)** directory contains user interface for application.

#####Configure Virtual Envoirnment#####
Inside this *ui* directory, run the following command.

`$> virtualenv venv`

This should give us a python virtual envoirnment.

Activate virtual envoirnment for python using,

`$> . venv/bin/activate`

Save current set of python application requirements using,

`$> pip freeze > requirements.txt`

Use the following to install required libraries for application to run,

This will read (-r flag) the requirements.txt file and install the required dependencies.

`$> pip install -r requirements.txt`
