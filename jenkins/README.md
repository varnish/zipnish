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
3. Install some jenkin plugins which you would/might required.
    + Amazon EC2 plugin
    + Amazon Web Services SDK
    + Ant Plugin
    + Artifact Deployer Plug-in
    + Build Pipeline Plugin
    + build timeout plugin
    + Build Timestamp Plugin
    + Copy Artifact Plugin
    + Copy To Slave Plugin
    + Credentials Plugin
    + CVS Plug-in
    + Deploy to container Plugin
    + Environment Injector Plugin
    + Exclusion Plug-in
    + Export Prameters
    + External Monitor Job Type Plugin
    + Git client plugin
    + Git Parameter Plug-In
    + Git plugin
    + Git server plugin
    + GitHub API Plugin
    + Github Authentication plugin
    + GitHub plugin
    + GitHub Pull Request Builder
    + GitHub Pull Request Plugin
    + instant-messaging plugin
    + IRC Plugin
    + Jackson 2 API Plugin
    + Javadoc Plugin
    + jQuery plugin
    + JUnit Plugin
    + LDAP Plugin
    + Mailer Plugin
    + MapDB API Plugin
    + Matrix Authorization Strategy Plugin
    + Matrix Project Plugin
    + Maven Integration plugin
    + Node Iterator API Plugin
    + OWASP Markup Formatter Plugin
    + PAM Authentication plugin
    + Parameterized Trigger plugin
    + Pipeline: Step API
    + Plain Credentials Plugin
    + Publish Over SSH
    + SCM API Plugin
    + Script Security Plugin
    + SSH Agent Plugin
    + SSH Credentials Plugin
    + SSH plugin
    + SSH Slaves plugin
    + SSH2 Easy Plugin
    + Subversion Plug-in
    + Terminate ssh processes
    + Token Macro Plugin
    + Translation Assistance plugin
    + Windows Slaves Plugin
    + Workspace Cleanup Plugin




