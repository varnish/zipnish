module.exports.parseChildrenServices = function(childService) {
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

module.exports.parseService = function(argService)
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
    service.children = this.parseChildrenServices( argService.substr(endIdx + 2) );
  }

  return service;
}

module.exports.parseServices = function(argServices)
{
  var services = [];

  for (var i = 0; i < argServices.length; i++) {
    services.push( this.parseService( argServices[i] ) );
  }

  return services;
}
