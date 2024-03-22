import os
import sys
import logging
import requests
import uvicorn
import fastapi
from nicegui import ui
from nicegui.events import ValueChangeEventArguments

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s %(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)
VERBOSITY = os.getenv("LOGGING_LEVEL")

word_language = os.getenv("WORD_LANGUAGE")

image_api_url = "https://api.unsplash.com/photos/random"
word_api_url = f"https://random-word-api.herokuapp.com/word?lang={word_language}"


class GetData:
    def __init__(self, image_api_url, word_api_url):
        self.image_api_url = image_api_url
        self.word_api_url = word_api_url

    # def get_imagedata(self):
    #     """Get the image data from API."""
    #     logger.debug("Getting image data...")

    #     image_data = requests.get(self.image_api_url).json()
    #     return image_data

    def get_word(self):
        """Get the word from API."""
        logger.debug("Getting a radom word...")

        word = requests.get(self.word_api_url).json()
        return word

class RenderPage:
    def show(event: ValueChangeEventArguments):
        name = type(event.sender).__name__
        ui.notify(f'{name}: {event.value}')

    ui.button('Button', on_click=lambda: ui.notify('Click'))
    with ui.row():
        ui.checkbox('Checkbox', on_change=show)
        ui.switch('Switch', on_change=show)
    ui.radio(['A', 'B', 'C'], value='A', on_change=show).props('inline')
    with ui.row():
        ui.input('Text input', on_change=show)
        ui.select(['One', 'Two'], value='One', on_change=show)
    ui.link('And many more...', '/documentation').classes('mt-8')

    ui.run()


def main():
    logger.setLevel(VERBOSITY)
    print(VERBOSITY)

    logger.debug("Server starting...")

    data = GetData(image_api_url, word_api_url)

    RenderPage(data)
    print(data.get_word())


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
