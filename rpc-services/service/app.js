var http = require('http');
var express = require('express');
var app = express();

var argv = require('minimist')(process.argv.slice(2));

console.log('argv.call', argv.call);

app.get('/', function (req, res) {

  var rpcCalls = [];

  if (argv.call) {
    if (Array.isArray(argv.call)) {
      rpcCalls = argv.call.slice();
    } else if (argv.call && argv.call.length) {
      rpcCalls.push( argv.call );
    }
  }

  if (rpcCalls.length > 0) {
    // single / multiple rpc calls
  } else {
    res.send(argv, service);
  }

});

var server = app.listen(argv.port, argv.address, function() {

  var address = server.address().address,
    port = server.address().port;

  console.log(argv.service + ' service listening at http://%s:%d', address, port);

});
