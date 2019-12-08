var Backbone = require('backbone'),
    Handlebars = require('handlebars'),

    Config = require('./../../util/config'),
    Log = require('./../../util/log'),
    DjangoUtil = require('./../../util/django-util'),

    Patient = require('./../../models/patients'),
    Schedules = require('./../../models/schedules'),
    MonitoringPatientView = require('./monitoring-patient'),
    MonitoringPatientDataView = require('./../monitoring-id/monitoring-patient-data');

var MonitoringTable = Backbone.View.extend({
  className: "dg-view dg-view-hide",
  initialize: function() {
    this.render();
    this.showAllPatients();
  },
  render: function() {
    var source = $('#tmp-monitoring-table').html(),
        template = Handlebars.compile(source),
        html = template();
    this.$el.html(html);
  },
  events: {
    'click .back': 'back',
    'change #filter-hospital': 'filterByHospital',
    'keyup #find-patient': 'findPatient'
  },

  monitoringPatientDataView: {},
  CollectionMonitoringPatientView: [],

  showPatientFromUrl: function( url ) {
    var that = this;

    DjangoUtil.getResults(url, [], function(patient) {
      Log("success = ", patient);
      for (var i = 0; i < patient.length; i++) {
        var patientModel = new Patient();
        patientModel.set(patient[i]);
        var monitoringPatientView = new MonitoringPatientView({
          model: patientModel
        });
        that.$el.find('tbody').append(monitoringPatientView.$el);
        that.CollectionMonitoringPatientView.push(monitoringPatientView);
      }
    });
  },
  showAllPatients: function() {
    this.showPatientFromUrl(Config.URL_API_PATIENTS);
  },
  showPatientData: function( id ) {
    Log('find patient with id = ', id);
    this.monitoringPatientDataView = new MonitoringPatientDataView();
    this.monitoringPatientDataView.setMonitoringTableView(this);
    this.monitoringPatientDataView.showPatientData(id);
  },
  clear: function() {
    for (var i = 0; i < this.CollectionMonitoringPatientView.length; i++) {
      this.CollectionMonitoringPatientView[i].remove();
    }
  },

  back: function() {
    this.monitoringPatientDataView.remove();
    this.$el.find('.table-patients').removeClass('hide table-patients-hide');
    this.$el.find('.patient-id').text('');
    this.$el.find('.title-table').removeClass('title-patient-data');
    Backbone.history.navigate( '/monitoreo/' );
  },
  filterByHospital: function(e) {
    var $element = $(e.target),
        value = $element.val(),
        url = Config.URL_API_PATIENTS + '?' + value;
    Log('monitoring-table: url = ', url);
    this.clear();
    this.$el.find('#find-patient').val('');
    this.showPatientFromUrl(url);
  },
  findPatient: function(e) {
    if(e.keyCode == 13) {
      var $element = $(e.target),
          value = $element.val(),
          url = Config.URL_API_PATIENTS + '?search=' + value;
      this.clear();
      this.$el.find('#filter-hospital').val('');
      this.showPatientFromUrl(url);
    }
  }
});

module.exports = MonitoringTable;