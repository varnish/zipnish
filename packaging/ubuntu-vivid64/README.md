```
$> export DEBFULLNAME="Muhammad Adeel"
$> export DEBEMAIL="adeel@varnish-software.com"

$> rm -rf /vagrant/tmp/ && mkdir -p /vagrant/tmp/ui/
$> cd /vagrant/ui/ && tar -cvzf /vagrant/tmp/ui/zipnish-ui.tar.gz . 2>&1 --exclude=venv
$> rm -rf /vagrant/tmp/ui/src/ && mkdir -p /vagrant/tmp/ui/src/ && cp -R /vagrant/ui/* /vagrant/tmp/ui/src/ && rm -rf /vagrant/tmp/ui/src/venv/
$> cd /vagrant/tmp/ui/ && bzr dh-make zipnish-ui 0.1 zipnish-ui.tar.gz
$> find /vagrant/tmp/ui/src/ -name "*.pyc" -exec rm -rf {} \;
```

Choose single and hit confirm after that.

```
$> rm -rf /vagrant/tmp/ui/zipnish-ui/debian/ && cp -R /vagrant/packaging/ubuntu-vivid64/debian/ /vagrant/tmp/ui/zipnish-ui/debian/

$> cd /vagrant/tmp/ui/zipnish-ui/ && debuild -us -uc -i -b
$> cd /vagrant/tmp/ui/ && rm -rf !(zipnish-ui_0.1-1_amd64.deb)
# apt-get remove -y zipnish-ui
# dpkg -i /vagrant/tmp/ui/zipnish-ui_0.1-1_amd64.deb
```



**When you are repeatedly building and testing below is a time saver**


$ rm -rf /vagrant/tmp/ui/zipnish-ui/debian/ && cp -R /vagrant/packaging/ubuntu-vivid64/debian/ /vagrant/tmp/ui/zipnish-ui/debian/ && cd /vagrant/tmp/ui/zipnish-ui/ && debuild -us -uc -i -b


# cd /vagrant/tmp/ui && apt-get remove -y zipnish-ui && dpkg -i /vagrant/tmp/ui/zipnish-ui_0.1-1_amd64.deb