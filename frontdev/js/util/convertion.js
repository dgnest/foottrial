var Convertion = {
  date: function ( value ) {
    // date format: yyyy-MM-dd'T'HH:mm:ss.SSSZ
    // date format: yyyy-MM-dd
    var date = new Date(value),
        arrDate = date.toLocaleString().split(/\/|,/, 3),
        mDate = arrDate[1] + '-' + arrDate[0] + '-' + arrDate[2];
    return mDate;
  }
};

module.exports = Convertion;