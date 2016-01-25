Setup virtual machine via vagrant.

```shell
$> vagrant init -m 'ubuntu/precise64'
$> vagrant up
```

Install jenkins. Instructions taken from [http://pkg.jenkins-ci.org/debian/](http://pkg.jenkins-ci.org/debian/)

```shell
# wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -
# echo "deb http://pkg.jenkins-ci.org/debian binary/" >> /etc/apt/sources.list
# apt-get update
# apt-get install -y jenkins
```

