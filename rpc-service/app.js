var http = require('http'),
  async = require('async'),
  express = require('express');

var app = express(),
  argv = require('minimist')(process.argv.slice(2));

// port : { key: value pairs }
var services = {
  5000: {
    service: 'Process Order'
  },

  5005: {
    service: 'Fetch Customer'
  },

  5010: {
    service: 'Fetch Products'
  },

  5011: {
    service: 'Get Payment Information'
  },

  5020: {
    service: 'Get Payment Information'
  },

  5021: {
    service: 'Validate Credit Card'
  },

  5022: {
    service: 'Verify Credit Card'
  },

  5031: {
    service: 'Approve Payment'
  },

  5051: {
    service: 'Update Inventory'
  },

  5052: {
    service: 'Update Order Status'
  },

  5053: {
    service: 'Send Order Email'
  },

  5054: {
    service: 'Update Order Shipping Status'
  }

};

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

    if (argv.flow === 'parallel') {

      async.parallel(funcs, function (err, results) {
        res.send('');
      });

    } else if (argv.flow === 'series') {

      async.series(funcs, function (err, results) {
        res.send('');
      });

    }

  } else {

    res.send(argv.service);

  }

});

var server = app.listen(argv.port, argv.address, function() {

  var address = server.address().address,
    port = server.address().port;

  console.log(argv.service + ' service listening at http://%s:%d', address, port);

});
