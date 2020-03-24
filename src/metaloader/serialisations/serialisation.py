from io import BufferedReader, BufferedWriter, TextIOWrapper, BytesIO
from abc import abstractmethod
from typing import BinaryIO, TextIO
from plugable import Plugable


class Serialisation(Plugable):
    """
        Represents a method of serialising a data structure
        within a file
    """

    EXTENSION = "dat"

    @classmethod
    def decode_import(cls, import_stmt: str):
        path = import_stmt.split(".")

        path[-1] = ".".join([path[-1], cls.EXTENSION])

        return path

    @abstractmethod
    def serialise(self, datastructure: dict, filestream: BinaryIO):
        raise NotImplementedError

    @abstractmethod
    def deserialise(self, filestream: BinaryIO) -> dict:
        raise NotImplementedError


class TextSerialisation(Serialisation):
    """
        Represents a method of serialising a data structure
        within a text-based file
    """

    def __init__(self, encoding: str = "utf-8"):
        self._encoding = encoding

    @abstractmethod
    def load(self, textstream: TextIO) -> dict:
        raise NotImplementedError

    @abstractmethod
    def dump(self, datastructure: dict, textstream: TextIO):
        raise NotImplementedError

    def serialise(self, datastructure: dict, filestream: BinaryIO) -> BinaryIO:
        buffer = BufferedWriter(filestream)

        kwargs = {
            "buffer": buffer,
            "encoding": self._encoding,
            "write_through": True
        }

        with TextIOWrapper(**kwargs) as textstream:
            self.dump(datastructure, textstream)
            buffer.flush()
            filestream.seek(0)
            return BytesIO(filestream.getvalue())

    def deserialise(self, filestream: BinaryIO):
        buffer = BufferedReader(filestream)
        with TextIOWrapper(buffer, self._encoding) as textstream:
            return self.load(textstream)
