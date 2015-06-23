var http = require('http'),
  async = require('async'),
  express = require('express');

var services = require('./services'),
    servicesParser = require('./services/parser');

var app = express(),
  argv = require('minimist')(process.argv.slice(2));

var servicesIndex = servicesParser.parseServices(argv.services);

app.get('/*', function (req, res) {

  services.findService(req.url, servicesIndex);

  res.send( req.url );

});

var server = app.listen(argv.port, argv.address, function() {

  var address = server.address().address,
    port = server.address().port;

  console.log(argv.service + ' server listening at http://%s:%d', address, port);

});
