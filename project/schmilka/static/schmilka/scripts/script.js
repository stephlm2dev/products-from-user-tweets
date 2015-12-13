$(document).ready(function() {

  var busy = false;
  $('#twittos').keypress(function() {
    var result = $(".twittos-list")
    var  input = $('#twittos').val()
    if ( input.length > 1 && !busy ) {
      busy = true;
      $.get('/schmilka/ajaxTwitterUser', { query: input }, function(data){
        if ( data.indexOf(";") != -1 ) {
          twittos = data.split(";")
          $('.twittos-list li').html( function(index) {
            $(this).addClass('not-empty');
            return '<button type="button">' + twittos[index] + '</button>';
          });
        }
      });
      busy = false;
    }
  });

  // FIMXE
  $('.twittos button').click( function() {
    var text = $(this).text();
    $('#twittos').val(text);
  });

});
