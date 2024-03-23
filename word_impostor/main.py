import os
import logging
from flask import Flask
from api import ImageDataResponse, WordDataResponse
from blueprints import rooms
from flask_socketio import SocketIO

logger = logging.getLogger(__name__)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO").upper()),
)


app = Flask(__name__)
app.config["SECRET_KEY"] = "batman"
app.register_blueprint(rooms.blueprint)
socketio = SocketIO(app)
rooms.register(socketio)


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    logger.info("Starting Game...")

    word_language = os.environ.get("WORD_LANGUAGE", "en")

    if os.environ.get("WORD_LANGUAGE") is None:
        logger.info("Language is not set. Defaulting to English.")
    else:
        logger.info("Language is set to '%s'", word_language)

    word_data = WordDataResponse(word_language)
    image_data = ImageDataResponse()

    socketio.run(app, host="0.0.0.0", port=5000)
