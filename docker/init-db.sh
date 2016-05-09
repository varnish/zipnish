#!/bin/bash

bind_to_localhost() {
  cat > /etc/mysql/my.cnf <<EOF
[mysql]
bind = 0.0.0.0
EOF
}

echo "******************* Start mysql ***************************"
service mysql start
sleep 1
echo "******************* Run database script *******************"
mysql -u root --password=rootpw < $db_script

echo "******************* Creating user *************************"
echo "CREATE USER '$user' IDENTIFIED BY '$password'" | mysql --default-character-set=utf8
echo "REVOKE ALL PRIVILEGES ON *.* FROM '$user'@'%'; FLUSH PRIVILEGES" | mysql --default-character-set=utf8
echo "GRANT SELECT ON *.* TO '$user'@'%'; FLUSH PRIVILEGES" | mysql --default-character-set=utf8
echo "GRANT ALL PRIVILEGES ON *.* TO '$user'@'%' WITH GRANT OPTION; FLUSH PRIVILEGES" | mysql --default-character-set=utf8

mysqladmin shutdown

echo "******************* Localhost bind ************************"
bind_to_localhost

echo "******************* Restart mysql *************************"
service mysql start

while true; do
    sleep 60
done
