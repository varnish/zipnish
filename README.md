# Tracking Micro-Services via Varnish Cache #

## Scope ##

Track timing of micro-service requests by passing micro-service requests through a varnish server.



## Varnish Log Script ##

For now the script merely checks and prints varnish log headers (key: value pairs).

Running the varnish logger script.

> &gt; cd log-reader

> &gt; python sample_varnishlog.py

## Installing or configuring jdk. ##

1. Download the jdk from: [http://www.oracle.com/technetwork/java/javase/downloads/index.html](http://www.oracle.com/technetwork/java/javase/downloads/index.html)
2. Create a folder "java" inside user home (e.g. /home/[username])
3. mv jdk from ~/Downloads to ~/java
4. extract jdk using tar zxvf **jdk-archive-name.tar.gz**
5. Use command > **update-alternatives --install /usr/bin/java java /home/[username]/java/jdk1.8.0_45/bin/java 1000** Note: name or path to jdk can vary depending on downloaded version.
6. choose default java version using > **update-alternatives --config java**
7. Similarly configure javac, > **update-alternatives --install /usr/bin/javac javac /home/[username]/java/jdk1.8.0_45/bin/javac 1000**
8. If needed configure default javac using, **update-alternatives --config javac**

## ZipKin ##

Running zipkin.

1. git clone git@github.com:twitter/zipkin.git
2. cd zipkin
3. run zipkind example using > **./bin/sbt "zipkin-example/run -zipkin.storage.anormdb.install=true -genSampleTraces=true"**
4. Once zipkin is installed and running, you can view the UI on: [http://localhost:8080](http://localhost:8080)
5. It is loaded with example data, and sqlite in memory database store.

## UI ##

Zipkin UI will be utilized for tracing request paths. UI can be accessed on: [http://localhost:8080](http://localhost:8080)

#### Request Tracking ####

- Trace 
  
  Represents a request path, contains one or more spans.

  - Span
    Span represents an RPC. It has,
    - **spanId** representing itself. 
    - **parentId** representing parent spanId. 
    - **traceId** linking it to the trace.
    - one or more **annotations**
    
    - Annotation
      - 

Trace contains multiple spans
Each span has a traceId linking it to the Trace.
Each span has a spanId identifying itself and parentId identifying parent span.
