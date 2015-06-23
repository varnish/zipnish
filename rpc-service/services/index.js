module.exports.findService = function (url, services) {

  var service = null;

  for (var i = services.length - 1; i >= 0; i--) {
    if (services[i].url && services[i].url === url) {
      return services[i];
    }
  }

  return null;
};
