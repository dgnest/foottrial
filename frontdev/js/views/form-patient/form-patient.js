var Backbone = require('backbone'),
    Handlebars = require('handlebars'),

    Log = require('./../../util/log'),
    Validation = require('./../../util/validation'),
    Config = require('./../../util/config'),

    CommonFormPatientView = require('./../common/form-patient'),
    PatienFormModalView = require('./form-patient-modal');

var FormPatientView = CommonFormPatientView.extend({
  initialize: function () {
    this.render();
    this.patienFormModalView = new PatienFormModalView({
      model: this.model
    });
    this.patienFormModalView.$el.appendTo('body');
    this.patienFormModalView.setFormPatientView(this);
  },
  events: {
    'change .dg-input': 'validateInput',
    'click .dg-submit': 'validate'
  },

  patienFormModalView: {},

  validate: function(e) {
    console.log(2);
    e.preventDefault();
    var inputs       = this.$el.find('.dg-input');
    var isValid      = true;
    var conta        = 0;
    var totalInput   = inputs.length;
    var ajaxValidate = function() {
      conta++;
      console.log('conta = %o, Total = %o', conta, totalInput);
      if (conta >= totalInput) {
        Log('form isValid = ' + isValid);
        if (isValid) {
          this.$el.find('.alert-danger').addClass('hide');
          this.patienFormModalView.show();
        } else {
          this.$el.find('.alert-danger').removeClass('hide');
        }
      }
    };

    for (var i = 0; i < inputs.length; i++) {
      var element       = inputs[i];
      var modelName     = element.name;
      var modelValue    = element.value;
      var mAjaxValidate = ajaxValidate.bind(this);

      this.model.set(modelName, modelValue);
      this.validation.bind(this)( modelName, modelValue, $(element), function(mIsValid) {
        isValid &= mIsValid;
        mAjaxValidate();
      });
    }

  },
  reset: function() {
    var inputs = this.$el.find('.dg-input');
    this.model.set(this.model.defaults);
    this.render();
  }
});

module.exports = FormPatientView;
