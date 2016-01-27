#!/usr/bin/env bash

wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -

if [ ! -f /etc/apt/sources.list.d/jenkins.list ]; then
	echo 'deb http://pkg.jenkins-ci.org/debian binary/' > /etc/apt/sources.list.d/jenkins.list
	apt-get update
	apt-get install -y jenkins
fi

# jenkins jar file
JENKINS_JAR="/var/cache/jenkins/war/WEB-INF/jenkins-cli.jar"
JENKINS_URL="http://127.0.0.1:8080/"

#update jenkins plugins
# UPDATE_LIST=$(java -jar $JENKINS_JAR -s $JENKINS_URL list-plugins | grep -e ')$' | awk '{ print $1 }');
# if [ ! -z "${UPDATE_LIST}" ]; then 
#     echo Updating Jenkins Plugins: ${UPDATE_LIST}; 
#     java -jar ${JENKINS_JAR} -s ${JENKINS_URL} install-plugin ${UPDATE_LIST};
#     java -jar ${JENKINS_JAR} -s ${JENKINS_URL} safe-restart;
# fi

# required plugins
# PLUGINS_TO_INSTALL=("amazon-ec2-plugin" "amazon-web-services-sdk" "ant-plugin" "artifact-deployer-plug-in" "build-pipeline-plugin" "build-timeout-plugin" "build-timestamp-plugin" "copy-artifact-plugin" "copy-to-slave-plugin" "credentials-plugin" "cvs-plug-in" "deploy-to-container-plugin" "environment-injector-plugin" "exclusion-plug-in" "export-prameters" "external-monitor-job-type-plugin" "git-client-plugin" "git-parameter-plug-in" "git-plugin" "git-server-plugin" "github-api-plugin" "github-authentication-plugin" "github-plugin" "github-pull-request-builder" "github-pull-request-plugin" "instant-messaging-plugin" "irc-plugin" "jackson-2-api-plugin" "javadoc-plugin" "jquery-plugin" "junit-plugin" "ldap-plugin" "mailer-plugin" "mapdb-api-plugin" "matrix-authorization-strategy-plugin" "matrix-project-plugin" "maven-integration-plugin" "node-iterator-api-plugin" "owasp-markup-formatter-plugin" "pam-authentication-plugin" "parameterized-trigger-plugin" "pipeline:-step-api" "plain-credentials-plugin" "publish-over-ssh" "scm-api-plugin" "script-security-plugin" "ssh-agent-plugin" "ssh-credentials-plugin" "ssh-plugin" "ssh-slaves-plugin" "ssh2-easy-plugin" "subversion-plug-in" "terminate-ssh-processes" "token-macro-plugin" "translation-assistance-plugin" "windows-slaves-plugin")

# for plugin in $PLUGINS_TO_INSTALL; do
# 	java -jar ${JENKINS_JAR} -s ${JENKINS_URL} install-plugin "$plugin";
# done
# java -jar ${JENKINS_JAR} -s ${JENKINS_URL} safe-restart;


