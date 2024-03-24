import uuid
from flask import Blueprint, render_template, request

rooms = set()

blueprint = Blueprint(
    "rooms",
    __name__,
    template_folder="templates",
    url_prefix="/room"
)


@blueprint.route("/create", methods=["POST"])
def create_room():
    error = request.args.get("error", "")

    return render_template("create_room.html", error=error)


@blueprint.route("/play/<name>")
def room(name):
    return render_template("play.html", room_name=name)


def register(socketio):
    @socketio.on("join_room")
    def join_room(json):
        print("join_room: " + str(json))

    @socketio.on("user_join")
    def handle_user_join(username):
        print(f"User {username} joined!")
        users[username] = request.sid

    @socketio.on("send_message")
    def communication(json):
        print("sent_message: " + str(json))
        socketio.emit("message", json)
