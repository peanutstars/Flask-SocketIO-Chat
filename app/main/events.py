import json
import sys
import time

from flask import session, request
from flask_socketio import emit, join_room, leave_room, Namespace
from .. import socketio


# @socketio.on('joined', namespace='/chat')
# def joined(message):
#     """Sent by clients when they enter a room.
#     A status message is broadcast to all people in the room."""
#     room = session.get('room')
#     join_room(room)
#     print(f'@@ JOIN: {session.get("name")} - "{message}"')
#     emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)
#     print(f'----------------------------------------')
#     sys.stdout.flush()

# @socketio.on('text', namespace='/chat')
# def text(message):
#     """Sent by a client when the user entered a new message.
#     The message is sent to all people in the room."""
#     room = session.get('room')
#     emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


# @socketio.on('left', namespace='/chat')
# def left(message):
#     """Sent by clients when they leave a room.
#     A status message is broadcast to all people in the room."""
#     room = session.get('room')
#     leave_room(room)
#     emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)


class ChatNamespace(Namespace):
    
    def on_connect(self):
        # 여기서 disconnect() 를 호출해도 연결이 끊어지지 않는다.
        # 이 콜백이 리턴되어야 disconnect가 가능 한 것 같다.
        name = session.get("name")
        print(f'@@ Connected: {name}')
    
    def on_disconnect(self):
        print(f'@@ Disconnected: {session.get("name")} {session.get("room")}')
        
    def on_joined(self, message):
        """Sent by clients when they enter a room.
        A status message is broadcast to all people in the room."""
        print(f">> session: {session}")
        name = session.get("name")
        room = session.get('room')
        if None in [name, room]:
            self.disconnect(request.sid)
            return
        join_room(room)
        print(f'@@ JOIN: {session.get("name")} - "{message}"')
        emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)

    def on_text(self, message):
        """Sent by a client when the user entered a new message.
        The message is sent to all people in the room."""
        room = session.get('room')
        emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)
    
    def on_left(self, message):
        """Sent by clients when they leave a room.
        A status message is broadcast to all people in the room."""
        room = session.get('room')
        leave_room(room)
        emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)
        
socketio.on_namespace(ChatNamespace('/chat'))
