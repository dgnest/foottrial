var Backbone = require('backbone');

var Route = Backbone.Router.extend({
  routes: {
    '': 'getHome',
    'ingresar/': 'getFormPatient',
    'pacientes/': 'getPacients',
    'pacientes/:id/': 'getPacientById',
    'monitoreo/': 'getMonitoring',
    'monitoreo/:id/': 'getMonitoringById'
  }
});

module.exports = Route;
