import typing
from abc import abstractmethod
from plugable import Plugable

from ..exceptions import ExclusiveStanzaClashError
from ..loader_context import LoaderContext


class StanzaHandler(Plugable):
    def __init__(self, key: str, exclusive=False):
        self.key = key
        self.exclusive = exclusive
        self.filenames = []
        self._includes = 0

    def _can_merge(self):
        if self.exclusive and self._includes > 1:
            return False
        return True

    def include(self, ctx: LoaderContext, new_data):
        self.filenames.append(ctx.current_filename)
        self._includes += 1
        if self._can_merge():
            if self.key not in ctx.data:
                ctx.data[self.key] = self._initialise()
            self._merge(ctx.data[self.key], new_data)
        else:
            clashing_files = ",".join(self.filenames)
            raise ExclusiveStanzaClashError(self.key, clashing_files)

    @abstractmethod
    def is_valid(self, new_data) -> bool:
        raise NotImplementedError

    @abstractmethod
    def _initialise(self):
        raise NotImplementedError

    @abstractmethod
    def _merge(self, stanza_data: dict, new_data):
        raise NotImplementedError

    def cleanup(self):
        self.filenames = []
        self._includes = 0


class TypedStanzaHandler(StanzaHandler):
    @property
    @abstractmethod
    def _type(self) -> typing.Type:
        raise NotImplementedError

    def _initialise(self):
        return self._type()

    def is_valid(self, new_data):
        if isinstance(new_data, self._type):
            return True
        return False
