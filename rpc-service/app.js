var http = require('http'),
  async = require('async'),
  express = require('express');

var app = express(),
  argv = require('minimist')(process.argv.slice(2));

console.log( argv.services );



var server = app.listen(argv.port, argv.address, function() {

  var address = server.address().address,
    port = server.address().port;

  console.log(argv.service + ' service listening at http://%s:%d', address, port);

});
