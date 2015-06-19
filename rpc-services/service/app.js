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

  console.log('inside service:', argv.service);

  if (rpcCalls.length > 0) {

    var funcs = [];

    for (var i = 0; i < rpcCalls.length; i++) {
      funcs.push((function (url) {

        return function(next) {

          http.get(url, function (res) {
            next();
          });

        };

      }( rpcCalls[i] )));
    }

    async.parallel(funcs, function (err, results) {
      console.log('parallel finishes');
    });

    res.send();

  } else {

    res.send(argv.service);

  }

});

var server = app.listen(argv.port, argv.address, function() {

  var address = server.address().address,
    port = server.address().port;

  console.log(argv.service + ' service listening at http://%s:%d', address, port);

});
