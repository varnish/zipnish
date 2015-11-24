How to create packages
-----

The packaging of both the LogReader and the UI components is based on spec files found here:

 > **Path:** zipnish/log-reader/redhat/log-reader.spec
 
 > **Path:** zipnish/ui/redhat/zipnish-ui.spec 

Create your required package by using the rpmbuild command:

*Example:*
```sh
$ rpmbuild -bb specfile
```

Prerequisites for runing LogReader and UI services
-----

The following is a set of required packages:

```sh
$ sudo yum install python-pip
$ sudo yum install mysql-devel
$ sudo yum install python-devel
```

After having the above installed, use PIP to install the rest of the required packages

```sh
$ sudo pip install simplemysql
$ sudo pip install crochet
$ sudo pip install flask
$ sudo pip install flask-sqlalchemy
$ sudo pip install flask-script
```

Run LogReader and UI services
-----

Install the LogReader and UI packages and run the following commands:

```sh
$ sudo service log-reader start
$ sudo service zipnish-ui start
```



