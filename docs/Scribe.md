## Scribe ##

[Scribe](https://github.com/facebookarchive/scribe) is a server for aggregating log data streamed in real time from a large number of servers.

1. git clone git@github.com:traviscrawford/scribe.git
2. sudo apt-get -y install autoconf ruby ruby-dev python python-dev libevent-dev install libboost-all-dev
7. Thrift
  * **pre-install requirements** 
  * > sudo apt-get -y install libboost-dev libboost-test-dev libboost-program-options-dev libevent-dev automake libtool flex bison pkg-config g++ libssl-dev
  * Download thrift from [http://www.apache.org/dyn/closer.cgi?path=/thrift/0.9.2/thrift-0.9.2.tar.gz](http://www.apache.org/dyn/closer.cgi?path=/thrift/0.9.2/thrift-0.9.2.tar.gz)
  * > cd /usr
  * > su
   * > Enter your password
 * > mkdir thrift
 * > cd thrift
 * > mv /home/debian/Downloads/thrift-0.9.2.tar.gz .
 * > tar zxvf thrift-0.9.2.tar.gz
 * > cd thrift-0.9.2
 * make
 * sudo make install
 * thrift -version
  * should output Thrift version 0.9.2
* install fb303 it's inside contrib/fb303 inside the thrift-0.9.2 directory
* apt-get install -y gawk
* cd contrib/fb303 (assuming you are inside thrift-0.9.2 installation directory)
* ./bootstrap.sh
* ./configure
* make install
