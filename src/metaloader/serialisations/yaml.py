from typing import TextIO
from ruamel.yaml import YAML
from .serialisation import TextSerialisation


class YamlSerialisation(TextSerialisation, register="yaml"):
    EXTENSION = "yaml"
    _YAML = YAML(typ="unsafe", pure=True)

    def dump(self, datastructure: dict, textstream: TextIO):
        self._YAML.dump(datastructure, textstream)

    def load(self, textstream: TextIO) -> dict:
        return self._YAML.load(textstream)
