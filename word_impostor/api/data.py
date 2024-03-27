import logging
import requests

logger = logging.getLogger(__name__)


class ImageDataResponse:
    """Get the image data."""

    URL = "https://picsum.photos/600"

    def __init__(self):
        logger.debug("Getting image data...")

    def get_image(self):
        logger.debug("Getting a random word...")

        image = requests.get(self.URL, timeout=10)
        return image


class WordDataResponse:
    """Get the word from API."""

    def __init__(self, word_language: str = "en"):
        self.url = (
            "https://random-word-api.herokuapp.com/word?" +
            f"lang={word_language}"
        )

        logger.debug("Getting image data...")
        logger.debug("Language: %s", word_language)

    def get_word(self):
        logger.debug("Getting a random word...")

        word = requests.get(self.url, timeout=10).json()
        return word
