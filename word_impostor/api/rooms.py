import uuid
import json
from flask_socketio import SocketIO, join_room
from coolname import generate_slug
from flask_restful import Resource
from flask import request


class Room:
    def __init__(self, room_name: str):
        self.name = room_name
        self.players = {}

    def add_player(self, client_id: str, player_id: str):
        self.players[client_id] = player_id

    def del_player(self, client_id: str):
        self.players.pop(client_id)

    def list_players(self):
        return [
            player_names[identifier] for identifier in self.players.values()
        ]


rooms: dict[str, Room] = {}

player_names = {}


class CreateRoom(Resource):
    def post(self):
        room_name = str(generate_slug(3))
        rooms[room_name] = Room(room_name)

        return {"room_name": room_name}, 200


class CreateUser(Resource):
    def post(self, username: str):
        if username:
            identifier = uuid.uuid4().hex
            player_names[identifier] = username

            return {"player_id": identifier}, 200

        return {"error": "No username provided"}, 400


def register(socketio: SocketIO):
    @socketio.on("join_game")
    def join_game(data):
        room_name = data.get("room_name")
        player_id = data.get("player_id")

        room = rooms.get(room_name)

        if not player_id or not room_name or not room:
            socketio.emit('error', 'validation')
            return

        room.add_player(request.sid, player_id)

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
