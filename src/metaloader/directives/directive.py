from abc import abstractmethod
from plugable import Plugable
from ..loader_context import LoaderContext


class Directive(Plugable):
    @abstractmethod
    def handle_directive(self, context: LoaderContext, args):
        pass


class ListDirective(Directive):
    @abstractmethod
    def handle_item(self, context: LoaderContext, item):
        pass

    def handle_directive(self, context: LoaderContext, args: list):
        for item in args:
            self.handle_item(context, item)
