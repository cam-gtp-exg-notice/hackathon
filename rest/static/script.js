var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('message', function(msg) {
  $('#messages').append($('<p>').text(msg));
});
$('form').submit(function(event) {
  event.preventDefault();
  var message = $('#message').val();
  socket.emit('message', message);
  $('#message').val('').focus();
});
