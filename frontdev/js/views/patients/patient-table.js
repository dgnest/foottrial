var Backbone = require('backbone'),
    Handlebars = require('handlebars'),
    _ = require('underscore'),

    Config = require('./../../util/config'),
    Log = require('./../../util/log'),
    DjangoUtil = require('./../../util/django-util');

    Patient = require('./../../models/patients'),
    PatientView = require('./patient'),
    PatientDataView = require('./../patients-id/patient-data');

var PatientTableView = Backbone.View.extend({
  className: "dg-view dg-view-hide",
  initialize: function() {
    this.render();
    this.getAllPatients();
  },
  render: function() {
    var source = $('#tmp-patient-table').html(),
        template = Handlebars.compile(source),
        // html = template(this.model.toJSON());
        html = template();
    this.$el.html(html);
  },
  events: {
    'click .back': 'showTable',
    'change .dg-filter': 'filterTable',
    'keypress #find-patient': 'findPatient',
    'click .sort': 'sortPatients'
  },

  patientsView: [],
  patientDataView: {},
  patientDataFormView: {},

  hideTable: function( callback ) {
      this.$el.find('.filter-container').hide();
      this.$el.find('.table-patients')
      .addClass('table-patients-hide')
      .one(
        'webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
        function(e) {
          $(e.target).addClass('hide');
          callback();
        }
      );
  },
  showTable: function(e) {
    e.preventDefault();
    e.stopPropagation();
    // Set patientDataFormView from patientDataView
    this.patientDataFormView = this.patientDataView.patientDataForm;
    if ( !_.isEmpty(this.patientDataFormView) ) {
      this.$el.find('.title-table').removeClass('title-patient-data-form');
      this.patientDataFormView.remove();
      this.patientDataView.patientDataForm = {};
      this.patientDataView.$el.show();
      Backbone.history.navigate('/pacientes/' + this.patientDataView.model.get('id') + "/");

    } else if ( !_.isEmpty(this.patientDataView) ) {
      this.$el.find('.filter-container').show();
      this.$el.find('.title-table').removeClass('title-patient-data');
      this.patientDataView.remove();
      this.$el.find('.show').hide();
      this.$el
        .find('.table-patients')
        .removeClass('table-patients-hide')
        .removeClass('hide');

      Backbone.history.navigate('/pacientes/');
    }
  },
  cleanTable: function() {
    for (var i = 0; i < this.patientsView.length; i++) {
      this.patientsView[i].remove();
    }
  },
  getFilterQuery: function() {
    var filterHospital = this.$el.find('#filter-hospital').val(),
        filterActive = this.$el.find('#filter-active').val();

    return "?" + filterHospital + "&" + filterActive;
  },
  filterTable: function() {
    var url = Config.URL_API_PATIENTS + this.getFilterQuery();
    this.$el.find('.sort i').removeClass('fa-sort-asc fa-sort-desc').addClass('fa-sort');
    this.getPatientFromUrl( url );
  },
  findPatient: function(e) {
    if(e.which == 13) {
      var $element = $(e.target),
          value = $element.val(),
          url = Config.URL_API_PATIENTS + "?code=" + value;
      this.getPatientFromUrl(url);
    }
  },
  getAllPatients: function() {
    this.getPatientFromUrl( Config.URL_API_PATIENTS + "?is_active=True" );
  },
  getPatientFromUrl: function( url ) {
    Log('url = ', url);
    this.cleanTable();
    var that = this;

    DjangoUtil.getResults(url, [], function(patient) {
      Log('data = ', patient);
      for (var i = 0; i < patient.length; i++) {
        var patientModel = new Patient();
        patientModel.set(patient[i]);
        var patientView = new PatientView({
          model: patientModel
        });
        that.patientsView.push(patientView);
        that.$el.find('tbody').append(patientView.$el);
      }
    });
  },
  showPatientData: function( id ) {
    Log('find patient with id = ', id);
    var that = this;

    $.ajax({
      url: Config.URL_API_PATIENTS + id + '/',
      type: 'GET',
      dataType: 'json'
    })
    .done(function(data) {
      // Put patient id title
      that.$el.find('.patient-id').text(data.code);
      that.$el.find('.title-table').addClass('title-patient-data');

      var patient = new Patient();
      patient.set(data);
      that.patientDataView = new PatientDataView({
        model: patient
      });
      that.patientDataView.patientTable = that;
      that.hideTable( function() {
        that.$el.find('.card.patients').append(that.patientDataView.$el);
        getComputedStyle(that.patientDataView.$el.find('.patient-data')[0]).opacity;
        that.patientDataView.$el.find('.patient-data').removeClass('patient-data-hide');

      } );
    })
    .fail(function() {
      Log("error");
    });
  },
  sortPatients: function(e) {
    var $element = $(e.currentTarget),
        sortBy = $element.data('sort-by'),
        sort = $element.data('sort'),
        url = Config.URL_API_PATIENTS + this.getFilterQuery() + '&ordering=';

    this.$el.find('.sort i').removeClass('fa-sort-asc fa-sort-desc').addClass('fa-sort');
    if ( sort === 'ascendent' ) {
      url += '+';
      $element.data('sort', 'descendent');
      $element.find('i').addClass('fa-sort-asc');
    } else if ( sort === 'descendent' ) {
      url += '-';
      $element.data('sort', 'ascendent');
      $element.find('i').addClass('fa-sort-desc');
    } else {
      url += '-';
      $element.data('sort', 'ascendent');
      $element.find('i').addClass('fa-sort-desc');
    }
    url += sortBy;
    this.getPatientFromUrl(url);
  }
});

module.exports = PatientTableView;
