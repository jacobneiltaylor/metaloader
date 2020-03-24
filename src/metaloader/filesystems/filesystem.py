from abc import abstractmethod
from typing import BinaryIO
from plugable import Plugable


class Filesystem(Plugable):
    def __init__(self):
        self._history = []

    @abstractmethod
    def get_filename(self, *args) -> str:
        pass

    @abstractmethod
    def _open(self, filename: str) -> BinaryIO:
        pass

    @abstractmethod
    def exists(self, filename: str) -> bool:
        pass

    def canonicalise(self, relative_filename: str):
        absolute_fn = self.get_filename(relative_filename)
        if self.exists(absolute_fn):
            return absolute_fn
        raise FileNotFoundError(absolute_fn)

    def open(self, filename) -> BinaryIO:
        self._history.append(filename)
        return self._open(filename)

    @property
    def history(self):
        return tuple(self._history)
