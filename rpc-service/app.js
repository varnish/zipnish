var timers = require('timers'),
    http = require('http'),
    querystring = require('querystring'),
    async = require('async'),
    express = require('express');

var services = require('./services'),
    servicesParser = require('./services/parser');

var app = express(),
  argv = require('minimist')(process.argv.slice(2));

var servicesIndex = servicesParser.parseServices(argv.services);

function getRandomTimeForDelay()
{
  // wait between 0 - 1.5 records before delivering any results back
  //return (Math.random() * 1.5).toFixed(2) * 1000;
  return 0;
}

app.get('/:serviceName/:indentLevel?', function (req, res) {

  var indentLevel = req.params.indentLevel ? parseInt(req.params.indentLevel) : 0,
      service = services.findService('/' + req.params.serviceName, servicesIndex);


  var randomTimeInSeconds, date;

  date = new Date();

  if (service) {

    /*
    console.log(Array(10).join('-'),
                date.getMinutes() + ':' + date.getSeconds() + ':' + date.getMilliseconds(), 

                Array(indentLevel * 3).join(' '), 
                service.label, '->', service.url);
    */

    var X_Varnish, X_Varnish_Trace, headers;

    X_Varnish = req.headers['x-varnish'];

    if (req.headers['x-varnish-trace']) {
      X_Varnish_Trace = req.headers['x-varnish-trace'];
    } else {
      X_Varnish_Trace = X_Varnish;
    }

    headers = {
      'x-varnish-trace': X_Varnish_Trace,
      'x-varnish-parent': X_Varnish
    };

    //console.log('trace =', X_Varnish_Trace, ', id =', X_Varnish, service.url);
    console.log('trace = %s, parent = %s, id = %s, url = %s', req.headers['x-varnish-trace'], req.headers['x-varnish-parent'], req.headers['x-varnish'], service.url);

    if (service.children) {
      var funcs = [],
          urlParams = (indentLevel + 1);

      for (var i = 0; i < service.children.urls.length; i++) {

        funcs.push(function(path) {

          return function (next) {
            http.get({
              'hostname': argv['address'],
              'port': argv['proxy-port'],
              'path': path,
              'agent': false,
              'headers': headers
            } , function (res) {

              //console.log('trace =', X_Varnish_Trace, ', id =', X_Varnish, path);

              timers.setTimeout(function() {
                next();
              }, getRandomTimeForDelay());

            });

          };

        }( service.children.urls[i]) );
      }

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

      timers.setTimeout(function() {
        res.send();
      }, getRandomTimeForDelay());

    }

  } else {
    res.status(404).send();
  }

});

var server = app.listen(argv.port, argv.address, function() {

  var address = server.address().address,
    port = server.address().port;

  console.log(argv.service + ' server listening at http://%s:%d', address, port);
  console.log('');

});
