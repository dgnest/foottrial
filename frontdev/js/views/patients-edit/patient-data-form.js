var Backbone = require('backbone'),
    Handlebars = require('handlebars'),

    Config = require('./../../util/config'),

    PatientDataFormModal = require('./patient-data-form-modal'),
    CommonFormPatientView = require('./../common/form-patient');

var PatientDataFormView = CommonFormPatientView.extend({
  className: 'dg-view',
  initialize: function() {
    this.render();
  },
  render: function() {
    Handlebars.registerHelper('selected', function(hospital, value) {
      return hospital == value ? ' selected' : '';
    });
    var source = $('#tmp-patient-data-form').html(),
        template = Handlebars.compile(source),
        html = template(this.model.toJSON());
    this.$el.html(html);
  },
  events: {
    'change .dg-input': 'validateInput',
    'click .dg-submit': 'editPatient'
  },

  isEditing: true,

  updateModel: function() {
      var inputs = this.$el.find('.dg-input');

      for (var i = 0; i < inputs.length; i++) {
        var name = $(inputs[i]).attr('name');
        this.model.set( name , $(inputs[i]).val() );
      }
  },
  editPatient: function() {
    this.updateModel();

    var patientDataFormModal = new PatientDataFormModal({
      model: this.model,
    });

    $('body').append(patientDataFormModal.$el);
    patientDataFormModal.show();
  }
});

module.exports = PatientDataFormView;
