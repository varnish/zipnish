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
    res.send( service.label );
  } else {
    res.status(404).send();
  }

});

var server = app.listen(argv.port, argv.address, function() {

  var address = server.address().address,
    port = server.address().port;

  console.log(argv.service + ' server listening at http://%s:%d', address, port);

});
