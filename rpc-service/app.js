var http = require('http'),
  async = require('async'),
  express = require('express');

var app = express(),
  argv = require('minimist')(process.argv.slice(2));

var services = {};

function parseService(argService)
{
  var serviceURLAndLabel,
    startIdx, endIdx;


  endIdx = argService.indexOf('=>');

  if (endIdx > -1) {
    serviceURLAndLabel = argService.substr(0, endIdx);
  } else {
    serviceURLAndLabel = argService;
  }

  var service = {}, temp;

  temp = serviceURLAndLabel.split(':');
  service.url = temp[0];
  service.label = temp[1];

}

function parseServices(argServices)
{
  var service;

  for (var i = 0; i < argServices.length; i++) {
    service = parseService( argServices[i] );
  }

}

parseServices(argv.services);

var server = app.listen(argv.port, argv.address, function() {

  var address = server.address().address,
    port = server.address().port;

  console.log(argv.service + ' service listening at http://%s:%d', address, port);

});
