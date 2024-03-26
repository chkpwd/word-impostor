import uuid
import json
from flask_socketio import SocketIO, join_room
from coolname import generate_slug
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)


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

blueprint = Blueprint(
    "rooms",
    __name__,
    template_folder="templates",
    url_prefix="/room"
)


@blueprint.route("/create", methods=["GET", "POST"])
def set_username():
    error = request.args.get("error", "")
    room_name = request.args.get("room_name", "")

    if request.method == "POST":
        if not room_name:
            room_name = str(generate_slug(3))
            rooms[room_name] = Room(room_name)

        identifier = uuid.uuid4().hex

        player_names[identifier] = request.form.get("username")

        if not player_names[identifier]:
            del player_names[identifier]
            return redirect(url_for(
                "rooms.set_username",
                room_name=room_name,
                error="Username cannot be empty")
            )

        session["player_id"] = identifier

        return redirect(url_for("rooms.game_session", name=room_name))

    return render_template(
        "set_username.html",
        error=error,
        room_name=room_name
    )


@blueprint.route("/play/<name>")  # wrapper function
def game_session(name):
    player_id = session.get("player_id")
    username = player_names.get(player_id)

    if not player_id or not username:
        return redirect(url_for("rooms.set_username", room_name=name))

    session["room_name"] = name

    return render_template(
        "game_session.html",
        room_name=name,
        username=username,
        player_id=player_id
    )


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
