Log Storage processes log items as they are recieved. 

It stores log items by processing and categorizing them internally using (Span and Annotation) arrays.

Span and Annotation arrays work like a buffer. We can specify the minimal number of items that must be present inside a Span / Annotation array before it's flushed to Storage.

Current limitations are,

**Minimum number of spans before flushing:** 2
**Minimum number of annotations before flushing:** 4
