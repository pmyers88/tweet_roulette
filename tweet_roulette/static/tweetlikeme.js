var accounts = '';

// get a json array of usernames
$.ajax({
  async: false,
  type: 'get',
  dataType: 'json',
  url: '/account/',
  success: function(data) {
    accounts = data;
  }
});

function validate() {
  // remove any previous errors
  if($('#error').length) {
    $('#error').remove();
  }
  var re = new RegExp('^\\w{1,15}$');
  var username = $('#username').val();
  if(!re.test(username)) {
    $('<p id="error">Usernames can only have letters, numbers and underscores. Try another username.</p>')
      .insertAfter('form');
    $('#username').val('');
    return false;
  } else if($.inArray(username, accounts) != -1) {
    // redirect to the username url if it already exists
    window.location.href = '/account/' + username + '/';
    return false;
  } else {
    $('<p>Fetching tweets (this only needs to be done once per account) <img src="http://tweetlikeme.herokuapp.com/static/loader.gif"/></p>')
      .insertAfter('form');
    return true;
  }
}

$(document).ready(function() {
  $('#username').autocomplete({
    source: function(request, responseFunction) {
      var search = $.ui.autocomplete.escapeRegex(request.term);
      var matcher = new RegExp("^" + search, "i" );
      var data = $.grep(accounts, function(item,index) {
        return matcher.test(item);
      });
      responseFunction(data);
    },
    minLength: 0
  });
});
