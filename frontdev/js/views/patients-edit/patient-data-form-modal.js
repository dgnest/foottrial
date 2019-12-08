var Backbone = require('backbone'),
    Handlebars = require('handlebars'),

    Config = require('./../../util/config');

var PatientDataFormModal = Backbone.View.extend({
  initialize: function() {
    this.render();
  },
  render: function() {
    var source = $('#tmp-patient-data-form-modal').html(),
        template = Handlebars.compile(source),
        html = template(this.model.toJSON());
    this.$el.html(html);
  },
  events: {
    'click .btn-success': 'editPatient'
  },

  show: function() {
    $(this.el).find('#patient-data-form-modal').modal('show');
  },
  editPatient: function() {
    var data = this.model.toJSON(),
        idPatient = this.model.get('id'),
        url = Config.URL_API_PATIENTS + idPatient + '/',
        password = this.$el.find('#input-password').val();
    data.password = password;
    $.ajax({
      url: url,
      type: 'PATCH',
      dataType: 'json',
      data: data,
    })
    .done(function() {
      console.log("success");
      swal("Edicion correcta!", "El usuario fue editado correctamente!", "success");
      Backbone.history.navigate('/pacientes/' + idPatient, {trigger: true});
      location.reload();
    })
    .fail(function() {
      sweetAlert("Error", "Ingrese una contraseña correcta!", "error");
    });
  }
});

module.exports = PatientDataFormModal;