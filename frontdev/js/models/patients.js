var Backbone = require('backbone'),

    Convertion = require('./../util/convertion');


var Patient = Backbone.Model.extend({
  defaults: {
    'id': null,
    'code': '',
    'first_name': '',
    'dni': null,
    'cellphone': null,
    'birthday': '',
    'is_active': true,
    'deactivate_reason': '',
    'date_joined': '',
    'date_deactivate': '',
    'hospital': null,
    'sms_scheduled': null,
    'total_sms': null,
    'sms_received': null,
    'sms_failed': null,
    'calls_scheduled': null,
    'total_calls': null,
    'calls_answered': null,
    'calls_failed': null
  },
  initialize: function() {
    this.on('change:hospital', this.setHospitalName, this);
    this.on('change:date_joined', this.setDateJoinedConverted, this);
    this.on('change:birthday', this.setBirthdayConverted, this);
    this.on('change:date_deactivate', this.setDateDeactivateConverted, this);
    this.on('change:total_calls', this.setTotalCallSended, this);
    this.on('change:total_sms', this.setTotalSmsSended, this);
  },

  setHospitalName: function(model, value) {
    if ( value === 1 ) {
      model.set( 'hospital_name', 'Cayetano Heredia' );
    } else if( value === 2 ) {
      model.set( 'hospital_name', 'Arzobispo Loayza' );
    }
  },
  setDateJoinedConverted: function(model, value) {
    // date format: yyyy-MM-dd'T'HH:mm:ss.SSSZ
    if(value) {
      model.set( 'date_joined_converted', Convertion.date(value) );
    }
  },
  setBirthdayConverted: function(model, value) {
    // date format: yyyy-MM-dd
    if(value) {
      model.set( 'birthday_converted',  this.convertDate(value) );
    }
  },
  setDateDeactivateConverted: function(model, value) {
    // date format: yyyy-MM-dd'T'HH:mm:ss.SSSZ
    if(value) {
      model.set( 'date_deactivate_converted', Convertion.date(value) );
    } else {
      model.set( 'date_deactivate_converted', '-' );
    }
  },
  setTotalCallSended: function(model, value) {
    model.set(
      'total_calls_sended',
      model.get('calls_answered') + model.get('calls_failed')
    );
  },
  setTotalSmsSended: function(model, value) {
    model.set(
      'total_sms_sended',
      model.get('sms_received') + model.get('sms_failed')
      );
  },

  convertDate: function( date ) {
    // date format: yyyy-MM-dd'T'HH:mm:ss.SSSZ
    var arrDate = date.split(/-|T/, 3),
        mDate = arrDate[2] + '-' + arrDate[1] + '-' + arrDate[0];
    return mDate;
  }
});

module.exports = Patient;
