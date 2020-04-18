from abc import abstractmethod
from typing import BinaryIO
from plugable import Plugable


class Filesystem(Plugable):
    def __init__(self):
        self._history = []

    @abstractmethod
    def get_filename(self, path, base=None) -> str:
        raise NotImplementedError

    @abstractmethod
    def _open(self, filename: str) -> BinaryIO:
        raise NotImplementedError

    @abstractmethod
    def exists(self, filename: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_dir_name(self, filename) -> str:
        raise NotImplementedError

    def canonicalise(self, relative_filename: str):
        absolute_fn = self.get_filename([relative_filename])
        if self.exists(absolute_fn):
            return absolute_fn
        raise FileNotFoundError(absolute_fn)

    def open(self, filename) -> BinaryIO:
        self._history.append(filename)
        return self._open(filename)

    @property
    def history(self):
        return tuple(self._history)
