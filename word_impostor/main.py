import os
import logging
from flask import Flask, render_template
from api import ImageDataResponse, WordDataResponse
from blueprints import rooms
from flask_socketio import SocketIO

logger = logging.getLogger(__name__)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO").upper()),
)

app = Flask(__name__, template_folder='templates')
app.config["SECRET_KEY"] = "batman"
app.register_blueprint(rooms.blueprint)
socketio = SocketIO(app)
rooms.register(socketio)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    logger.info("Starting Game...")

    word_language = os.environ.get("WORD_LANGUAGE", "en")
    listen_address = os.environ.get("ADDRESS", "0.0.0.0")
    listen_port = os.environ.get("PORT", 5000)

    if os.environ.get("WORD_LANGUAGE") is None:
        logger.info("Language is not set. Defaulting to English.")
    else:
        logger.info("Language is set to '%s'", word_language)

    if os.environ.get("ADDRESS") is None:
        logger.info("Address is not set. Defaulting to 0.0.0.0.")
    else:
        logger.info("Address is set to '%s'", listen_address)

    if os.environ.get("PORT") is None:
        logger.info("Port is not set. Defaulting to 5000.")
    else:
        logger.info("Port is set to '%s'", listen_port)

    word_data = WordDataResponse(word_language)
    image_data = ImageDataResponse()

    socketio.run(app, host="0.0.0.0", port=5000)
