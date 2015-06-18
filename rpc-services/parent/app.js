var express = require('express');
var app = express();

app.get('/', function (req, res) {
  res.send('Parent Service');
});

var server = app.listen(3000, '127.0.0.1', function() {
  var address = server.address(),
    host = address.address,
    port = address.port;

  console.log('Parent app listening at http://%s:%s', host, port);
});
