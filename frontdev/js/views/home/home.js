var Backbone = require('backbone'),
Handlebars = require('handlebars'),
_ = require('underscore'),

Config = require('./../../util/config'),
Log = require('./../../util/log'),
DjangoUtil = require('./../../util/django-util');

require('./../../vendor/highstock');

var Home = Backbone.View.extend({
  className: "dg-view dg-view-hide",
  initialize: function() {
    this.listenTo(this.model, "change", this.render);
    this.showKpi();
    this.showChart();
  },
  render: function() {
    var source = $('#tmp-home').html(),
        template = Handlebars.compile(source),
        html = template(this.model.toJSON());
    this.$el.html(html);
  },

  showKpi: function() {
    var url = Config.URL_API_SCHEDULES + "?exclude_response_status=SCHEDULED",
        that = this;

    DjangoUtil.getResults(
      url,
      [],
      function( result ) {
        Log('home:: result = ', result);
        var callTotal = _.where( result, {type_message: 'CALL'} ),
            callFailed = _.where( callTotal, {response_status: 'FAILED'} ),
            callMax = _.max(callTotal, function(call){ return parseFloat(call.call_time); }),
            callMin = _.min(callTotal, function(call){ return parseFloat(call.call_time); }),
            callAverage = 0,

            smsTotal = _.where( result, {type_message: 'SMS'} ),
            smsFailed = _.where( smsTotal, {response_status: 'FAILED'} );

        for (var i = 0; i < callTotal.length; i++) {
          callAverage += Math.round( parseFloat(callTotal[i].call_time)/callTotal.length * 100 ) / 100;
        }

        that.model.set({
          sms_total: smsTotal.length,
          sms_failed: smsFailed.length,
          sms_sent: smsTotal.length - smsFailed.length,

          call_total: callTotal.length,
          call_failed: callFailed.length,
          call_sent: callTotal.length - callFailed.length,
          call_min: callMin.call_time,
          call_max: callMax.call_time,
          call_average: Math.round(callAverage * 100) / 100
        });
      },
      function() {

      }
    );
  },
  showChart: function() {
    var url = Config.URL_API_SCHEDULES + "?exclude_response_status=SCHEDULED&type_message=SMS";
        that = this;

    DjangoUtil.getResults(
      url,
      [],
      function(result) {
        var smsSent = _.where( result, {response_status: 'SENT'} ),
            smsReceived = _.where( result, {response_status: 'RECEIVED'} ),
            smsSentJson = [],
            smsReceivedJson = [];

        for (var i = 0; i < smsSent.length; i++) {
          var date = new Date(smsSent[i].date_scheduled);
          smsSentJson.push([date , 1]);
        }

        for (var j = 0; j < smsReceived.length; j++) {
          var mDate = new Date(smsReceived[j].date_scheduled);
          smsReceivedJson.push([mDate , 1]);
        }

        that.createChart(smsSentJson, smsReceivedJson);
      },
      function() {

      }
    );
  },
  createChart: function( smsSentJson, smsReceivedJson ) {
    $(this.el).find('#highstock-container').highcharts('StockChart', {
      rangeSelector: {
        selected: 4
      },

      plotOptions: {
        series: {
          compare: 'value'
        }
      },

      tooltip: {
        pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
        valueDecimals: 2
      },

      series: [
        {
          name: 'Mensajes Enviados',
          data: smsSentJson
        },
        {
          name: 'Mensajes Recibidos',
          data: smsReceivedJson
        }
      ]
    });
  }
});

module.exports = Home;