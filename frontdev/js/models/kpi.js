var Backbone = require('backbone');

var Kpi = Backbone.Model.extend({
  defaults: {
    "sms_total": 0,
    "sms_sent": 0,
    "sms_failed": 0,
    "call_total": 0,
    "call_sent": 0,
    "call_failed": 0
  },
});

module.exports = Kpi;