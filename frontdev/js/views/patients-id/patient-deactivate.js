var Backbone = require('backbone'),
    Handlebars = require('handlebars'),

    Config = require('./../../util/config');

var PatientDeactivate = Backbone.View.extend({
  initialize: function() {
    this.render();
  },
  render: function() {
    var source = $('#tmp-patient-deactivate').html(),
        template = Handlebars.compile(source),
        html = template();
    this.$el.html(html);
  },
  events: {
    'click .dg-deactivate': 'deactivate',
    'change .dg-input': 'validate'
  },

  validate: function(e) {
    this.validateInput( $(e.target) );
  },
  validateInput: function($element) {
    var isValid = true,
        mValidate = function ( mIsValid, $element ) {
          if ( mIsValid ) {
            $element.parents('.form-group').removeClass('has-error');
            isValid = true;
          } else {
            $element.parents('.form-group').addClass('has-error');
            isValid = false;
          }
        };

    switch( $element.attr('name') ) {
      case 'reason':
        mValidate( $element.val() !== "0", $element );
        break;
      case 'password':
        mValidate( $element.val() !== "", $element );
        break;
    }

    return isValid;
  },
  isValid: function() {
    var inputs = this.$el.find('.dg-input'),
        isValid = true;

    for (var i = 0; i < inputs.length; i++) {
      isValid &= this.validateInput( $(inputs[i]) );
    }

    return isValid;
  },
  show: function() {
    this.$el.appendTo('body');
    $(this.el).find('#patient-deactivate-modal').modal('show');
  },
  deactivate: function() {
    var that = this,
        url = Config.URL_API_PATIENTS + this.model.get('id') + '/',
        data = {
          is_active: false,
          deactivate_reason: this.$el.find('#input-reason').val(),
          password: this.$el.find('#input-password').val()
        };

    if ( !this.isValid() ) {
      return;
    }

    $.ajax({
      url: url,
      type: 'PATCH',
      dataType: 'json',
      data: data,
    })
    .done(function() {
      console.log('success');
      swal({
        title: 'Quitado de seguimiento exitoso',
        text: 'Se quito exitosamente el seguimiento al paciente ' + that.model.get('code') + ', ya no se le mandará ningun mensaje a partir de ahora',
        type: 'success',
        closeOnConfirm: true
      }, function(){
        $(that.el).find('#patient-deactivate-modal').modal('hide');
        that.remove();
        Backbone.history.navigate('pacientes/', {trigger: true});
      });
    })
    .fail(function() {
      swal("¿Es un infiltrado?", "Parece que no es usted, por favor ingrese su contraseña correctamente", "error");
    });

  }
});

module.exports = PatientDeactivate;