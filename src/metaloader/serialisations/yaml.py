from typing import TextIO
from ruamel import yaml
from .serialisation import TextSerialisation


class YamlSerialisation(TextSerialisation, register="yaml"):
    EXTENSION = "yaml"

    def dump(self, datastructure: dict, textstream: TextIO):
        yaml.dump(datastructure, textstream, yaml.Dumper)

    def load(self, textstream: TextIO) -> dict:
        return yaml.load(textstream, yaml.Loader)
