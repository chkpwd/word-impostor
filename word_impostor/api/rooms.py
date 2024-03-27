from coolname import generate_slug
from flask_restful import Resource

rooms: dict[str, "Room"] = {}  # instantiate first before class is available

class Room:
    def __init__(self, room_name: str):
        self.name = room_name
        self.players = {}

    def add_player(self, client_id: str, username: str):
        self.players[client_id] = username

    def get_player(self, client_id: str):
        return self.players.get(client_id)

    def del_player(self, client_id: str):
        self.players.pop(client_id)

    def list_players(self):
        return list(self.players.values())

class CreateRoom(Resource):
    def post(self):
        room_name = str(generate_slug(3))
        rooms[room_name] = Room(room_name)

        return {"room_name": room_name}, 200

