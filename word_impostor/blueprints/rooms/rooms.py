from flask import Blueprint, render_template, request, redirect, url_for

rooms = set()

blueprint = Blueprint(
    "rooms",
    __name__,
    template_folder="templates",
    url_prefix="/room"
)


@blueprint.route("/list")
def list_rooms():
    return render_template("list_rooms.html", rooms=rooms)


@blueprint.route("/create", methods=["GET", "POST"])
def create_room():
    error = request.args.get("error", "")

    if request.method == "POST":
        room_name = request.form["room_name"]

        if room_name in rooms:
            # Redirect based on the flask blueprint and function name
            return redirect(url_for(
                "rooms.create_room",
                error="Room already exists")
            )
        else:
            rooms.add(room_name)
            return redirect(url_for("rooms.room", name=room_name))

    return render_template("create_room.html", error=error)


@blueprint.route("/play/<name>")
def room(name):
    return render_template("play.html", room_name=name)


def register(socketio):
    @socketio.on("join_room")
    def join_room(json):
        print("join_room: " + str(json))

    @socketio.on("send_message")
    def communication(json):
        print("sent_message: " + str(json))
        socketio.emit("message", json)
