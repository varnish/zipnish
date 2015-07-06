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

app.get('/:serviceName/:indentLevel?', function (req, res) {

  var indentLevel = req.params.indentLevel ? parseInt(req.params.indentLevel) : 0,
      service = services.findService('/' + req.params.serviceName, servicesIndex);


  var randomTimeInSeconds, date;

  date = new Date();

  // wait between 0 - 1.5 records before delivering any results back
  randomDelayTimeInSeconds = (Math.random() * 1.5).toFixed(2) * 1000;

  if (service) {

    console.log(Array(30).join('-'));
    console.log(date.getMinutes() + ':' + date.getSeconds() + ':' + date.getMilliseconds(), Array(indentLevel * 3).join(' '), service.label, '->', service.url);

    if (service.children) {
      var funcs = [],
          urlParams = (indentLevel + 1);

      for (var i = 0; i < service.children.urls.length; i++) {

        funcs.push(function(path) {

          return function (next) {

            http.get('http://' + argv.address +':'+ argv['proxy-port'] + path, function (res) {
              next();
            });

          };

        }( service.children.urls[i]) );
      }

      //console.log('>> flow', '-', service.children.flow);

      if (service.children.flow === 'serial') {

        async.series(funcs, function (err, results) {

          timers.setTimeout(function() {
            res.send();
          }, randomDelayTimeInSeconds);

        });

      } else if (service.children.flow === 'parallel') {

        async.parallel(funcs, function (err, results) {

          timers.setTimeout(function() {
            res.send();
          }, randomDelayTimeInSeconds);

        });

      }
    } else {

      timers.setTimeout(function() {
        res.send();
      }, randomDelayTimeInSeconds);

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
