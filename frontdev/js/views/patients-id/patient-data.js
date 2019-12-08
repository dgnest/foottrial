var Backbone = require('backbone'),
    Handlebars = require('handlebars'),

    Log = require('./../../util/log'),

    PatientDeactivateView = require('./patient-deactivate'),
    PatientDataForm = require('./../patients-edit/patient-data-form');

var PatientData = Backbone.View.extend({
  className: 'clearfix',
  initialize: function() {
    this.render();
  },
  render: function() {
    var source = $('#tmp-patient-data').html(),
        template = Handlebars.compile(source),
        html = template(this.model.toJSON());
    this.$el.html(html);
  },
  events: {
    'click .edit': 'showForm',
    'click .deactivate': 'showDeactivateModal'
  },

  patientTable: {},
  patientDataForm: {},

  showForm: function() {
    // Show 'edit' in the title
    this.patientTable.$el.find('.title-table').addClass('title-patient-data-form');

    this.patientDataForm = new PatientDataForm({
      model: this.model
    });
    $('.card.patients').append(this.patientDataForm.$el);
    this.$el.hide();
    Backbone.history.navigate( '/pacientes/' + this.model.get('id') + '/edit' );
  },
  showDeactivateModal: function() {
    Log('patient-data:: Show form to deactivate patient');
    var patientDeactivateView = new PatientDeactivateView({
      model: this.model
    });
    patientDeactivateView.show();
  }
});

module.exports = PatientData;
