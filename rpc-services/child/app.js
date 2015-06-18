var express = require('express');
var app = express();

app.get('/', function (req, res) {
  res.send('Child Service');
});

var server = app.listen(4000, '127.0.0.1', function() {
  var address = server.address(),
    host = address.address,
    port = address.port;

  console.log('Child service listening at http://%s:%s', host, port);
});
