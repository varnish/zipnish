var express = require('express');
var app = express();

var argv = require('minimist')(process.argv.slice(2));

app.get('/', function (req, res) {
  res.send(argv.service + ' service');
});

var server = app.listen(argv.port, argv.address, function() {

  var address = server.address().address,
    port = server.address().port;

  console.log(argv.service + ' service listening at http://%s:%d', address, port);

});
