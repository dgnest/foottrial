var Backbone = require('backbone'),

    Convertion = require('./../util/convertion');

var Schedules = Backbone.Model.extend({
  defaults: {
    "message": null,
    "patient": null,
    "parsed_message": "",
    "type_message": null,
    "date_scheduled": null,
    "date_sent": null,
    "response_status": null,
    "call_time": null,
    "retries": null
  },
  initialize: function () {
    this.on('change:message_details', this.setTypeMessageName, this);
    this.on('change:date_sent', this.setDateScheduledConverted, this);
  },

  setTypeMessageName: function( model, value ) {
    typeMessage = value.type_message;
    if ( typeMessage === 'R' ) {
      model.set( 'type_message_name', 'Recordatorio' );
    } else if ( typeMessage === 'M' ) {
      model.set( 'type_message_name', 'Motivacional' );
    }
  },
  setDateScheduledConverted: function( model, value ) {
    model.set( 'date_scheduled_converted', Convertion.date(value) );
  }
});

module.exports = Schedules;