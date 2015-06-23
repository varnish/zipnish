var http = require('http'),
  async = require('async'),
  express = require('express');

var parser = require('./services/parser');

var app = express(),
  argv = require('minimist')(process.argv.slice(2));

var services = parser.parseServices(argv.services);

console.log( services );


app.get('/*', function (req, res) {

  //var service = global.findService(req.url);

  req.send( req.url );

});

var server = app.listen(argv.port, argv.address, function() {

  var address = server.address().address,
    port = server.address().port;

  console.log(argv.service + ' service listening at http://%s:%d', address, port);

});
