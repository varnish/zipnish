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

  - Span represents an RPC. It has,
  
    - **spanId** representing itself. 
    - **parentId** representing parent spanId. Absense means it's the rootSpan. A point from where trace starts.
    - **traceId** linking it to the trace.
    - one or more **annotations**
    
    - Annotation
      - Marks an occurance in time.
        - cs = time when client made the request.
        - sr = time when server recieved the request.
        - ss = time when server sent the response.
        - cr = time when client recieved the response.
        
        cs -> sr -> ss -> cr

        - cr marks the end of an RPC call.
      
      - **Binary Annotations** are time independent and provides extra information about an RPC.
      
Each of the id's are randomly generated and are 64-bits long. **traceId** is only generated once and can be the same as the initial **spanId**. 

On the same RPC **spanId** is re-used during cs / sr / ss / cr (see above). 

Making RPC call downstream will require a newly generated **spanId**. Each downstream call made will have a **spanId** from the RPC caller, it's called **parentId**

Each downstream RPC call will inherit **spanId** RPC call initiater.

Additional headers e.g. **Sampled** value either 0 or 1 is passed. **Sampled** allows RPC call to determine if it should record trace information (1) or not (0). Pre-assuming the flag values, 1 and 0 as yes and no.


#### Collecting Data ####

SpanReciever daemon inside ZipKin is responsible for collecting data, validating it and passing it to storage.

ZipKin has a Scribe reciever. [Scribe](https://github.com/facebookarchive/scribe) is a framework for aggregating log data.

#### Solution Process ####

Idea would be to send all data to Scribe. Then use Scribe SpanReciever inside ZipKin to collection all tracing data and log information.
