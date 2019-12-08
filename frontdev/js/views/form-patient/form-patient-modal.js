var Backbone   = require('backbone');
var Handlebars = require('handlebars');
var Config     = require('./../../util/config');
var swal       = require('sweetalert');

require('./../../util/ajax-util');


var PatientFormModal = Backbone.View.extend({
  initialize: function() {
    this.render();
    // this.listenTo(this.model, "change", this.render);
  },
  render: function() {
    var source = $('#tmp-form-patient-modal').html(),
        template = Handlebars.compile(source),
        html = template(this.model.toJSON());
    this.$el.html(html);
  },
  events: {
    'click .dg-submit-modal': 'submit'
  },

  formPatientView: {},

  show: function() {
    console.log('model = %o', this.model.toJSON());
    this.render();
    $(this.el).find('#pacient-form-modal').modal('show');
  },
  changeDate: function (date) {
    var mDate = date.split('/');
    // be: dd/mm/YYYY
    // should be: YYYY-mm-dd
    return mDate[2] + "-" + mDate[1] + "-" + mDate[0];
  },
  setFormPatientView: function( mFormPatientView ) {
    this.formPatientView = mFormPatientView;
  },

  submit: function() {
    var data = this.model.toJSON(),
        $this = $(this.el);
        formPatientView = this.formPatientView;
    data.birthday = this.changeDate(data.birthday_converted);

    var $buttons = this.$el.find('.btn:enabled');
    $buttons.attr('disabled', 'disabled');

    console.log('submit');

    $.ajax({
      url: Config.URL_API_PATIENTS,
      type: 'POST',
      dataType: 'json',
      data: data,
    })
    .done(function(data) {
      $buttons.removeAttr('disabled');
      console.log("success");
      $this.find('#pacient-form-modal').modal('hide');
      swal("Paciente Ingresado", "El paciente " + data.code + " fué ingresado exitósamente", "success");
      formPatientView.reset();
    })
    .fail(function(e) {
      console.log("error ");
      swal("Error", "Hubo un problema ingresando al paciente " + data.code + "\n" + e.responseText, "error");
    });

  }
});

module.exports = PatientFormModal;
