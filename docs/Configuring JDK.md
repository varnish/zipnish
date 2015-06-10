## Installing or configuring jdk. ##

1. Download the jdk from: [http://www.oracle.com/technetwork/java/javase/downloads/index.html](http://www.oracle.com/technetwork/java/javase/downloads/index.html)
2. Create a folder "java" inside user home (e.g. /home/[username])
3. mv jdk from ~/Downloads to ~/java
4. extract jdk using tar zxvf **jdk-archive-name.tar.gz**
5. Use command > **update-alternatives --install /usr/bin/java java /home/[username]/java/jdk1.8.0_45/bin/java 1000** Note: name or path to jdk can vary depending on downloaded version.
6. choose default java version using > **update-alternatives --config java**
7. Similarly configure javac, > **update-alternatives --install /usr/bin/javac javac /home/[username]/java/jdk1.8.0_45/bin/javac 1000**
8. If needed configure default javac using, **update-alternatives --config javac**
