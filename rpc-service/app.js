var http = require('http'),
  async = require('async'),
  express = require('express');

var services = require('./services'),
    servicesParser = require('./services/parser');

var app = express(),
  argv = require('minimist')(process.argv.slice(2));

var servicesIndex = servicesParser.parseServices(argv.services);

app.get('/*', function (req, res) {

  var service = services.findService(req.url, servicesIndex);

  if (service) {
    //res.send( service.label );
    console.log(service.url, '->', service.label);

    if (service.children) {
      var funcs = [];

      for (var i = 0; i < service.children.urls.length; i++) {
        funcs.push(function(url) {

          return function (next) {
            http.get(url, function (res) {
              next();
            });
          };

        }(argv.proxy + service.children.urls[i]));
      }

      console.log('>> flow', '-', service.children.flow);

      if (service.children.flow === 'serial') {

        async.series(funcs, function (err, results) {
          res.send();
        });

      } else if (service.children.flow === 'parallel') {

        async.parallel(funcs, function (err, results) {
          res.send();
        });

      }
    } else {

      res.send();

    }

  } else {
    res.status(404).send();
  }

});

var server = app.listen(argv.port, argv.address, function() {

  var address = server.address().address,
    port = server.address().port;

  console.log(argv.service + ' server listening at http://%s:%d', address, port);

});
