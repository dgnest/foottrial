var Backbone = require('backbone'),
Route = require('./router/route'),
Log = require('./util/log'),

Patient = require('./models/patients'),
Kpi = require('./models/kpi'),

HomeView = require('./views/home/home'),
FormPatientView = require('./views/form-patient/form-patient'),
PatientTableView = require('./views/patients/patient-table'),
PatientDataView = require('./views/patients-id/patient-data'),
MonitoringTableView = require('./views/monitoring/monitoring-table');

var route = new Route(),
homeView,
formPatientView,
patientTableView,
monitoringTableView;

var moveAside = function() {
  var top = $(document).scrollTop(),
  header = $('header').height(),
  mTop = header - top;

  if ( mTop > 0 ) {
    $('.sidebar').removeClass('sidebar-fixed');
  } else {
    $('.sidebar').addClass('sidebar-fixed');
  }
};

// moveAside();
// $('aside').css('opacity', '1');

$(document).on("scroll", function(){
  moveAside();
});

var showAnimationCard = function( $element ) {
  setTimeout(function() {
    getComputedStyle($element[0]).margin-top;
    getComputedStyle($element[0]).opacity;
    $element.removeClass('dg-view-hide');
  }, 200);
};

var hideAnimationCard = function( view ) {
  view.$el.addClass('dg-view-hide');
  view.$el.one(
    'webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
    function(e) {
      view.remove();
    }
    );
};

var cleanView = function() {
  $("html, body").animate({ scrollTop: 0 }, 200);
  $('.nav-option').removeClass('active');
  if (homeView) {
    hideAnimationCard( homeView );
  }
  if (formPatientView) {
    hideAnimationCard( formPatientView );
  }
  if (patientTableView) {
    hideAnimationCard( patientTableView );
  }
  if (monitoringTableView) {
    hideAnimationCard( monitoringTableView );
  }
};

route.on('route:getHome', function() {
  Log('home');
  cleanView();
  $('#nav-home').addClass('active');
  var kpiModel = new Kpi();
  homeView = new HomeView({
    model: kpiModel
  });
  homeView.$el.appendTo('.dg-body');
  showAnimationCard(homeView.$el);
});

route.on('route:getFormPatient', function() {
  Log('ingresar');
  cleanView();
  $('#nav-pacient-form').addClass('active');
  $('#view-pacient-form').show();

  var patient = new Patient();
  formPatientView = new FormPatientView({
    model: patient
  });
  formPatientView.$el.appendTo('.dg-body');
  showAnimationCard(formPatientView.$el);
});

route.on('route:getPacients', function() {
  Log('pacientes');
  cleanView();
  $('#nav-pacients').addClass('active');

  patientTableView = new PatientTableView();
  patientTableView.$el.appendTo('.dg-body');
  showAnimationCard(patientTableView.$el);
});

route.on('route:getPacientById', function(id) {
  Log('pacientes id = ', id);
  if ( !patientTableView ) {
    cleanView();
    patientTableView = new PatientTableView();
    patientTableView.$el.appendTo('.dg-body');
    showAnimationCard(patientTableView.$el);
  }
  patientTableView.showPatientData(id);
  $('#nav-pacients').addClass('active');
});

route.on('route:getMonitoring', function() {
  Log('monitoreo');
  cleanView();
  $('#nav-monitoring').addClass('active');

  monitoringTableView = new MonitoringTableView();
  monitoringTableView.$el.appendTo('.dg-body');
  showAnimationCard(monitoringTableView.$el);
});

route.on('route:getMonitoringById', function(id) {
  Log('monitoreo id');
  if ( !monitoringTableView ) {
    cleanView();
    monitoringTableView = new MonitoringTableView();
    monitoringTableView.$el.appendTo('.dg-body');
    showAnimationCard(monitoringTableView.$el);
  }
  monitoringTableView.showPatientData(id);
  $('#nav-monitoring').addClass('active');
});

Backbone.history.start({pushState: true});
// Backbone.history.navigate('', {trigger: true});

$('.nav-option').on('click', function(event) {
  event.preventDefault();
  /* Act on the event */
  var href = $(this).attr('href');
  Backbone.history.navigate(href, {trigger: true});
});
