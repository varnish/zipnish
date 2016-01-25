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

Once it's installed you will get a UI running on [http://192.168.38.15:8080/](http://192.168.38.15:8080/)

Then update jenkins.

1. [http://192.168.38.15:8080/manage](http://192.168.38.15:8080/manage)
2. Choose **Manage Plugins**. Select the plugins you want to update. After update **restart jenkins**. Option for restarting jenkins would be on the same page where you update jenkins.
3. Install plugins which would/might be required [list of plugins](plugins.md)




