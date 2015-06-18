var express = require('express');
var app = express();

var argv = require('minimist')(process.argv.slice(2));

app.get('/', function (req, res) {
  res.send('Parent Service');
});

var server = app.listen(argv.port, argv.address, function() {
  var address = server.address(),
    host = address.address,
    port = address.port;

  console.log('Parent app listening at http://%s:%s', host, port);
});
