from coolname import generate_slug
from flask import Blueprint, render_template, request, redirect, url_for

rooms = set()

blueprint = Blueprint(
    "rooms",
    __name__,
    template_folder="templates",
    url_prefix="/room"
)


@blueprint.route("/create", methods=["GET", "POST"])
def generate_room():
    error = request.args.get("error", "")

    if request.method == "POST":
        room_name = str(generate_slug(3))

        rooms.add(room_name)
        return redirect(url_for("rooms.room", name=room_name))
    return render_template("generate_room.html", error=error)


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
