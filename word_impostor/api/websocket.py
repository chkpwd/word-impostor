import json
from flask_socketio import SocketIO, join_room
from flask import request
from .rooms import rooms


def register(socketio: SocketIO):
    @socketio.on("join_game")
    def join_game(data):
        room_name = data.get("room_name")
        username = data.get("username")

        room = rooms.get(room_name)

        if not username or not room_name or not room:
            socketio.emit('error', 'validation')
            return

        room.add_player(request.sid, username)

        join_room(room_name)
        socketio.emit(
            'player_list',
            json.dumps(room.list_players()),
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

    @socketio.on("send_message")
    def communication(data):
        print("sent_message: " + str(data))
        socketio.emit("message", data)
