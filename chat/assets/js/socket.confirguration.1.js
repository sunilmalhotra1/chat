  var urlParams = new URLSearchParams(window.location.search);
  var roomId = urlParams.get('roomId');
  var receiverId = urlParams.get('receiverId');
  var senderId = urlParams.get('senderId');
  var socket = io.connect();

  socket.on('connect', function () {
      socket.emit('my_event', {
          data: 'I\'m connected!'
      });
  });
  socket.on('disconnect', function () {
      $('#log').append('<br>Disconnected');
  });
  socket.on('my_response', function (msg) {
      //$('#log').append('<br>Received: ' + msg.data);
      bindMessage(msg);
  });

  bindMessage = function (obj) {
      var message = obj.data;
      console.log(obj);
      var isIn = true;
      if (obj.senderId != undefined) {
          isIn = !(obj.senderId == senderId);
      }


      if (isIn) {
          var senderUi = `<li>
        <div class="message-data">
          <span class="message-data-name"><i class="fa fa-circle online"></i> Self</span>
          <span class="message-data-time">10:12 AM, Today</span>
        </div>
        <div class="message my-message">
        ${message}
        </div>
      </li>
      `;
          $('.msg_history').append(senderUi);
      } else {


          var receiveUi = `<li class="clearfix">
          <div class="message-data align-right">
            <span class="message-data-time">10:10 AM, Today</span> &nbsp; &nbsp;
            <span class="message-data-name">Other</span> <i class="fa fa-circle me"></i>
          </div>
          <div class="message other-message float-right">
          ${message}
          </div>
        </li>`;
          $('.msg_history').append(receiveUi);
      }
  }
  // event handler for server sent data
  // the data is displayed in the "Received" section of the page
  // handlers for the different forms in the page
  // these send data to the server in a variety of ways
  emit_data = function (dataMessage) {
      console.log('emit_data', dataMessage);
      socket.emit('my_event', {
          data: dataMessage
      });

  };
  broadcast_data = function (dataMessage) {
      console.log('broadcast_data', dataMessage);
      socket.emit('my_broadcast_event', {
          data: dataMessage
      });

  };
  join_room = function (roomId) {
      socket.emit('join', {
          room: roomId
      });

  };
  leave_room = function (roomId) {
      socket.emit('leave', {
          room: roomId
      });

  };
  send_room = function (data) {
      socket.emit('my_room_event', data);

  };
  closeRoom = function (roomId) {
      socket.emit('close_room', {
          room: roomId
      });

  };
  disconnect = function () {
      socket.emit('disconnect_request');

  };