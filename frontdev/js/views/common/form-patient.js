var Backbone = require('backbone'),
    Handlebars = require('handlebars'),

    Log = require('./../../util/log'),
    Validation = require('./../../util/validation'),
    Config = require('./../../util/config');

var FormPatientView = Backbone.View.extend({
  className: "dg-view dg-view-hide",
  render: function() {
    Handlebars.registerHelper('selected', function(hospital, value) {
      return hospital == value ? ' selected' : '';
    });
    var source = $('#tmp-form-patient').html(),
        template = Handlebars.compile(source),
        html = template(this.model.toJSON());
    this.$el.html(html);
  },

  isEditing: false,

  validation: function( modelName, modelValue, $element, callback ) {
    var isValid   = true;
    var mValidate = function (comparator, $element, error, url, errorUrl) {
      isValid = comparator;
      if (comparator) {
        $element.parent().parent().removeClass('has-error');
        $element.parents('.form-group').find('.error').addClass('hide');
      } else {
        $element.parent().parent().addClass('has-error');
        $element.parents('.form-group').find('.error').removeClass('hide').find('span').text(error);
      }

      if ( url && isValid ) {
        this.existPatientSameAttr( url, function( isValid ) {
          Log("same code = " + isValid);
          mValidate( isValid, $element, errorUrl );
          callback(isValid);
        });
      } else {
        callback(isValid);
      }
    };

    console.log('Model Name = %o, Model Value = %o', modelName, modelValue);

    switch( modelName ) {
      case 'first_name':
        var regex = /^([a-zA-Záéíóúñ]){1,}$/i;
        mValidate( regex.test(modelValue), $element, 'Ingrese un nombre correcto' );
        break;
      case 'dni':
        // var url = Config.URL_API_PATIENTS + "?dni=" + modelValue;
        if ( this.model.toJSON()[modelName] === modelValue && this.isEditing ) {
          mValidate.bind(this)(
            Validation.isDni(modelValue),
            $element,
            'Ingrese un DNI válido'
          );
        } else {
          regex = /^\d{8}$/g;
          mValidate.bind(this)(
            regex.test(modelValue),
            $element,
            'Ingrese un DNI válido'
          );
        }
        // else {
        //   mValidate.bind(this)(
        //     Validation.isDni(modelValue),
        //     $element,
        //     'Ingrese un DNI válido',
        //     url,
        //     'Ya existe un paciente con este DNI'
        //   );
        // }

        break;
      case 'code':
        // var url = Config.URL_API_PATIENTS + "?code=" + modelValue;
        regex = /^[\d]{1}-[\d]{3}$/g;
        if ( this.model.toJSON()[modelName] === modelValue && this.isEditing ) {
          mValidate.bind(this)(
            regex.test(modelValue),
            $element,
            'Ingrese un código correcto'
          );
        } else {
          mValidate.bind(this)(
            regex.test(modelValue),
            $element,
            'Ingrese un código correcto'
          );
        }
        // else {
        //   mValidate.bind(this)(
        //     regex.test(modelValue),
        //     $element,
        //     'Ingrese un código correcto',
        //     url,
        //     'Ya existe un paciente con este código'
        //   );
        // }
        break;
      case 'cellphone':
        // var url = Config.URL_API_PATIENTS + "?cellphone=" + modelValue;
        if ( this.model.toJSON()[modelName] === modelValue && this.isEditing ) {
          mValidate.bind(this)(
            Validation.isPhoneNumber(modelValue),
            $element,
            'Ingrese un número celular correcto'
          );
        } else {
          regex = /^\d{9}$/g;
          mValidate.bind(this)(
            regex.test(modelValue),
            $element,
            'Ingrese un número celular correcto'
          );
        }
        // else {
        //   mValidate.bind(this)(
        //     Validation.isPhoneNumber(modelValue),
        //     $element,
        //     'Ingrese un número celular correcto',
        //     url,
        //     'Ya existe un paciente con este número celular'
        //   );
        // }
        break;
      case 'hospital':
        mValidate( modelValue !== '0', $element, 'Seleccione un hospital' );

        if ( modelValue === '1' ) {
          this.model.set( 'hospital_name', 'Cayetano Heredia' );
        } else if( modelValue === '2' ) {
          this.model.set( 'hospital_name', 'Arzobispo Loayza' );
        }
        break;
      case 'birthday':
        mValidate( Validation.isDate(modelValue), $element, 'Ingrese una fecha válida' );
        break;
      case 'birthday_converted':
        regex = /^([1-9]|[0-2][0-9]|3[0-1])\/([1-9]|0[1-9]|1[0-2])\/\d{4}$/g;
        mValidate( regex.test(modelValue), $element, 'Ingrese una fecha válida dd/mm/aaaa' );
        break;
      default:
        callback(true);
        break;
    }
  },
  validateInput: function(e) {
    Log('validate input = ', e.target);
    var $element = $(e.target),
        modelName = e.target.name,
        modelValue = e.target.value;

    this.validation( modelName, modelValue, $element, function(){} );
  },
  existPatientSameAttr: function( url, callback ) {
    $.ajax({
      url: url,
      type: 'GET',
      dataType: 'json'
    })
    .done(function( data ) {
      if ( data.count > 0 ) {
        callback(false);
      } else {
        callback(true);
      }
    })
    .fail(function() {
      Log("error getting patient with the same code");
    });

  }
});

module.exports = FormPatientView;
