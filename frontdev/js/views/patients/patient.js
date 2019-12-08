var Backbone = require('backbone'),
    Handlebars = require('handlebars'),

    Log = require('./../../util/log');

var PatientView = Backbone.View.extend({
  tagName: 'tr',
  initialize: function() {
    this.render();
    this.colour();
  },
  render: function() {
    var source = $('#tmp-patient').html(),
        template = Handlebars.compile(source),
        html = template(this.model.toJSON());
    this.$el.html(html);
  },
  events: {
    'click': 'viewPatient'
  },

  colour: function() {
    // Colour red if is not active patient
    if ( !this.model.get('is_active') ) {
      this.$el.addClass('error');
    }
  },
  viewPatient: function() {
    Backbone.history.navigate('/pacientes/' + this.model.get('id') + "/", {trigger: true});
  }
});

module.exports = PatientView;
