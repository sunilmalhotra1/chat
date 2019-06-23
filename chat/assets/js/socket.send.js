$(document).ready(function () {


    join_room(roomId);
    $(document).on('click', '.msg_send_btn', function () {
      var message = $('#message-to-send').val();

      var socketObj = { room: roomId, data: message, senderId: receiverId, receiverId: senderId,dateTime:moment().format('lll') };
      send_room(socketObj);
      $('#message-to-send').val('');
    });
  });