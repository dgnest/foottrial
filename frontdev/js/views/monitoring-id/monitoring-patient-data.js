var Backbone = require('backbone'),
    Handlebars = require('handlebars'),

    Config = require('./../../util/config'),
    Log = require('./../../util/log'),

    Schedules = require('./../../models/schedules'),
    CallScheduledView = require('./call-scheduled');

var MonitoringPatientData = Backbone.View.extend({
  initialize: function() {
    this.render();
  },
  render: function() {
    var source = $('#tmp-monitoring-patient-table').html(),
        template = Handlebars.compile(source),
        html = template();
    this.$el.html(html);
  },

  monitoringTableView: {},

  hideTable: function( callback ) {
      this.monitoringTableView.$el.find('.table-patients')
      .addClass('table-patients-hide')
      .one(
        'webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
        function(e) {
          $(e.target).addClass('hide');
          callback();
        }
      );
  },
  setMonitoringTableView: function (view) {
    this.monitoringTableView = view;
  },
  showPatientData: function ( idPatient ) {
    var url = Config.URL_API_SCHEDULES + '?type_message=CALL&patient=' + idPatient,
        that = this;

    // Put patient id title
    this.monitoringTableView.$el.find('.patient-id').text(window.monitoring_patient_code);
    this.monitoringTableView.$el.find('.title-table').addClass('title-patient-data');
    getComputedStyle(this.monitoringTableView.$el.find('.table-patients')[0]).opacity;

    this.hideTable( function() {
      that.monitoringTableView.$el.find('.card.monitoring').append(that.$el);
    });

    this.getList(
      url,
      [],
      function( scheduled ) {
        Log("monitoring-patient-data:: success = ", scheduled);
        if ( scheduled.length > 0 )
          that.monitoringTableView.$el.find('.patient-id').text(scheduled[0].patient_code);

        for (var i = 0; i < scheduled.length; i++) {
          if ( scheduled[i].response_status !== 'SCHEDULED' ) {
            var schedules = new Schedules();
            schedules.set(scheduled[i]);
            var callScheduledView = new CallScheduledView({
              model: schedules
            });
            that.$el.find('tbody').append(callScheduledView.$el);
          }
        }
      },
      function() {
        Log("error");
      }
    );
  },
  getList: function ( url, list, callback, callbackError ) {
    var that = this;
    $.ajax({
      url: url,
      type: 'GET',
      dataType: 'json'
    })
    .done( function ( data ) {
      var result = data.results;

      for (var i = 0; i < result.length; i++) {
        list.push(result[i]);
      }

      if (data.next) {
        that.getList( data.next, list, callback, callbackError );
      } else {
        callback(list);
      }
    })
    .fail( function () {
      callbackError();
    });
  }
});

module.exports = MonitoringPatientData;