## ZipKin ##

Running zipkin.

1. git clone git@github.com:twitter/zipkin.git
2. cd zipkin
3. run zipkin example using > **./bin/sbt "zipkin-example/run -zipkin.storage.anormdb.install=true -zipkin.storage.anormdb.db=sqlite://Users/[USERNAME]/Desktop/zipkin/logger.db -genSampleTraces=true"**
  * if you remove **-zipkin.storage.anormdb.db** option, zipkin uses mysql in-memory store.
    * if zipkin persistent store is used as in 3. above. Database for it will be found on /Users/[USERNAME]/Desktop/zipkin/logger.db
  * if you remove **-genSampleTraces=true** option, zipkin does not generate sample data.
  * for mysql - **./bin/sbt "zipkin-example/run -zipkin.storage.anormdb.install=true -zipkin.storage.anormdb.db=mysql://127.0.0.1:3306/zipkin?user=zipkin&password=kinect -genSampleTraces=true"**
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
