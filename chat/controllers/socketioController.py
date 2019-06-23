# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
import socketio
import os
from django.shortcuts import render
async_mode = None


basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(async_mode=async_mode)
thread = None


class ChatMessage:
    def __init__(self, room, receiverId, senderId, data):
        self.room = room
        self.receiverId = receiverId
        self.senderId = senderId
        self.data = data


def index(request):
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return render(request,'chat\\index.html')


def users(request):
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return render(request,'chat\\users.html')


def userschat(request):
    global thread
    roomId = request.GET.get('roomId', None)
    print(roomId)
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return render(request,'chat\\one.to.one.chat.html')


def userschatui(request):
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return render(request,'chat\\user.chat.html')


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('my_response', {'data': 'Server generated event'},
                 namespace='/test')


@sio.event
def my_event(sid, message):
    print(message)
    sio.emit('my_response', message, room=sid)


@sio.event
def my_broadcast_event(sid, message):
    sio.emit('my_response', message)


@sio.event
def join(sid, message):
    sio.enter_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
             room=sid)


@sio.event
def leave(sid, message):
    sio.leave_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Left room: ' + message['room']},
             room=sid)


@sio.event
def close_room(sid, message):
    sio.emit('my_response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'])
    sio.close_room(message['room'])


@sio.event
def my_room_event(sid, message):
    try:
        obj=ChatMessage(message['room'],message['receiverId'],message['senderId'],message['data'])
        sio.emit('my_response', obj, room=message['room'])
    except:
        sio.emit('my_response', message, room=message['room'])
    
    


@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)


@sio.event
def connect(sid, environ):
    sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.event
def disconnect(sid):
    print('Client disconnected')
