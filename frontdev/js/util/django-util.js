var djangoUtil = {
  getResults: function ( url, list, callback, callbackError ) {
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
        that.getResults( data.next, list, callback, callbackError );
      } else {
        callback(list);
      }
    })
    .fail( function () {
      callbackError();
    });
  }
};

module.exports = djangoUtil;