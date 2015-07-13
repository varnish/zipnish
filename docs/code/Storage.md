Log Storage processes log items as they are recieved. 

It stores log items by processing and categorizing them internally using (Span and Annotation) arrays.

Span and Annotation arrays work like a buffer. We can specify the minimal number of items that must be present inside a Span / Annotation array before it's flushed to Storage.
