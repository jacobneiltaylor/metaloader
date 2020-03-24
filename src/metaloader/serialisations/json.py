import json
from typing import TextIO
from .serialisation import TextSerialisation


class JsonSerialisation(TextSerialisation, register="json"):
    EXTENSION = "json"

    def dump(self, datastructure: dict, textstream: TextIO):
        json.dump(datastructure, textstream)

    def load(self, textstream: TextIO) -> dict:
        return json.load(textstream)
