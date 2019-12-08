var Validation = {
  isDni: function( dni ) {
    var regex = /(\b\d{8}\b)+$/g;
    return regex.test(dni);
  },
  isPhoneNumber: function( phoneNumber ) {
    var regex = /^\d{9}$/g;
    return regex.test(phoneNumber);
  },
  isDate: function( date ) {
    var regex = /\b\d{2}[/]?\d{2}[/]?\d{4}\b/i;
    return regex.test(date);
  }
};

module.exports = Validation;
