var Backbone = require('backbone'),
    Handlebars = require('handlebars'),

    Log = require('./../../util/log');

var MonitoringPatient = Backbone.View.extend({
  tagName: 'tr',
  initialize: function() {
    this.render();
  },
  render: function() {
    var source = $('#tmp-monitoring-patient').html(),
        template = Handlebars.compile(source),
        html = template(this.model.toJSON());
    this.$el.html(html);
  },
  events: {
    'click': 'viewPatient'
  },

  viewPatient: function() {
    window.monitoring_patient_code = this.model.get('code');
    Backbone.history.navigate('/monitoreo/' + this.model.get('id') + "/", {trigger: true});
  }
});

module.exports = MonitoringPatient;
