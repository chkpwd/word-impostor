import json
import flask_socketio
from flask import request
from .rooms import rooms

def error(socketio: flask_socketio.SocketIO, message: str):
    socketio.emit('error', message, to=request.sid)

def register(socketio: flask_socketio.SocketIO):
    @socketio.on("join_room")
    def join_room(data):
        if type(data) is not dict:
            # socketio.emit('error', 'Pls Data')
            error(socketio, 'Pls Data ' + str(data))
            return

        if data.get("room_name") not in rooms:
            # socketio.emit('error', 'Room not found')
            print("Room name")
            error(socketio, 'Room not found')
            return

        if data.get("username") is None:
            # socketio.emit('error', 'Username not found')
            error(socketio, 'Username not found')
            return

        room_name = data.get("room_name")
        username = data.get("username")

        room = rooms.get(room_name)
        room.add_player(request.sid, username)

        flask_socketio.join_room(room_name)
        socketio.emit(
            'player_list',
            json.dumps(room.list_players()),
            to=room_name
        )
        socketio.emit(
            'player_joined',
            json.dumps(room.get_player(request.sid)),
            to=room_name
        )

    @socketio.on("disconnect")
    def disconnect():
        for room in rooms.values():
            if request.sid in room.players:
                room.del_player(request.sid)
                socketio.emit(
                    'player_list',
                    json.dumps(room.list_players()),
                    to=room.name
                )
                socketio.emit(
                    'player_leave',
                    json.dumps(room.get_player(request.sid)),
                    to=room.name
                )

    @socketio.on("send_message")
    def communication(data):
        print("sent_message: " + str(data))
        socketio.emit("message", data)
