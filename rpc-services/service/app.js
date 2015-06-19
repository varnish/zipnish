var http = require('http'),
  async = require('async'),
  express = require('express');

var app = express(),
  argv = require('minimist')(process.argv.slice(2));

app.get('/', function (req, res) {

  var rpcCalls = [];

  if (argv.call) {
    if (Array.isArray(argv.call)) {
      rpcCalls = argv.call.slice();
    } else if (argv.call && argv.call.length) {
      rpcCalls.push( argv.call );
    }
  }

  console.log('Inside service:', argv.service);

  if (rpcCalls.length > 0) {

    res.send(argv.service);

  } else {

    res.send(argv.service);

  }

});

var server = app.listen(argv.port, argv.address, function() {

  var address = server.address().address,
    port = server.address().port;

  console.log(argv.service + ' service listening at http://%s:%d', address, port);

});
