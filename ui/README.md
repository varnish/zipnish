User interface for log reader.

#####Install bower (if not already installed)#####

[http://bower.io/#install-bower](http://bower.io/#install-bower)

#####Installing Frontend Dependencies#####

`$> cd ui/resources`

`$> bower install`

#####System#####

**[app](app/)** directory contains application. Written in flask.

**[user interface](ui/)** directory contains user interface for application.

####Configure Virtual Envoirnment####
Inside this *ui* directory, run the following command.

`$> virtualenv venv`

This should give us a python virtual envoirnment.

Activate virtual envoirnment for python using,

`$> . venv/bin/activate`

Save current set of python application requirements using,

`$> pip freeze > requirements.txt`

Use the following to install required libraries for application to run,

This will read (-r flag) the requirements.txt file and install the required dependencies.

`$>pip install -r requirements.txt`
