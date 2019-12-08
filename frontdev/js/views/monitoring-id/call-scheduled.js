var Backbone = require('backbone'),
    Handlebars = require('handlebars');

var MonitoringPatientData = Backbone.View.extend({
  tagName: 'tr',
  initialize: function() {
    this.colour();
    this.render();
  },
  render: function() {
    var source = $('#tmp-monitoring-call-scheduled').html(),
        template = Handlebars.compile(source),
        html = template(this.model.toJSON());
    this.$el.html(html);
  },

  colour: function() {
    // Colour red if is FAILED
    if ( this.model.get('response_status') === 'FAILED' ) {
      this.$el.addClass('error');
      this.model.set('call_time', 'No Contestó');
    }
  }
});

module.exports = MonitoringPatientData;