var http = require('http'),
  async = require('async'),
  express = require('express');

var app = express(),
  argv = require('minimist')(process.argv.slice(2));

function parseChildrenServices(childService)
{
  var callFlow, childServices, childrenURLs, temp;

  temp = childService.split(':');

  callFlow = temp[0];
  childrenURLs = temp[1].split(',');

  var data = {
    flow: callFlow,
    urls: childrenURLs
  };

  return data;
}

function parseService(argService)
{
  var serviceURLAndLabel, startIdx, endIdx, hasChildrenServices;


  hasChildrenServices = false;
  endIdx = argService.indexOf('=>');

  if (endIdx > -1) {
    hasChildrenServices = true;
    serviceURLAndLabel = argService.substr(0, endIdx);
  } else {
    serviceURLAndLabel = argService;
  }

  var service = {}, temp;

  temp = serviceURLAndLabel.split(':');
  service.url = temp[0];
  service.label = temp[1];

  if (hasChildrenServices) {
    service.children = parseChildrenServices( argService.substr(endIdx + 2) );
  }

  return service;
}

function parseServices(argServices)
{
  var services = [];

  for (var i = 0; i < argServices.length; i++) {
    services.push( parseService( argServices[i] ) );
  }

  return services;
}

var services = parseServices(argv.services);

app.get('/*', function (req, res) {

  res.send( req.url );


});

var server = app.listen(argv.port, argv.address, function() {

  var address = server.address().address,
    port = server.address().port;

  console.log(argv.service + ' service listening at http://%s:%d', address, port);

});
