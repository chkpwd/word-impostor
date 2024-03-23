import os
import sys
import logging
import requests
from flask import Flask

class ImageDataResponse:
    """Get the image data."""

    URL = "https://picsum.photos/600"

    def __init__(self):
        logging.debug("Getting image data...")

    def get_image(self):
        """Get the image from Picsum."""
        image = requests.get(self.URL, timeout=10).json()
        return image

class WordDataResponse:
    """Get the word from API."""

    def __init__(self, word_language: str = "en"):
        self.url = f"https://random-word-api.herokuapp.com/word?lang={word_language}"

        logging.debug("Getting image data...")
        logging.debug("Language: %s", word_language)

    def get_word(self):
        logging.debug("Getting a random word...")

        word = requests.get(self.url, timeout=10).json()
        return word

class RenderSite:
    """Render the page with the image and word."""

    def __init__(self):
        self.image_data = ImageDataResponse()
        self.word_data = WordDataResponse()

    def render_page(self):
        """Render the page with the image and word."""
        app = Flask(__name__)

        @app.route('/')
        def hello():
            return self.word_data.get_word()

def main():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO").upper()),
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    logging.info("Starting Game...")

    word_language = os.environ.get("WORD_LANGUAGE", "en")

    if os.environ.get("WORD_LANGUAGE") is None:
        logging.info("Language is not set. Defaulting to English.")
    else:
        logging.info("Language is set to '%s'", word_language)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
