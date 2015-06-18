var express = require('express');
var app = express();

var argv = require('minimist')(process.argv.slice(2));

console.log(argv);

app.get('/', function (req, res) {
  res.send(argv.service + ' service');
});

var server = app.listen(argv.port, argv.host, function() {
  var address = server.address(),
    host = address.address,
    port = address.port;

  console.log(argv.service + ' service listening at http://%s:%s', host, port);
});
