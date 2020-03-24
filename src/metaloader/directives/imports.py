from .directive import ListDirective
from ..loader_context import LoaderContext


class ImportsDirective(ListDirective, register="imports"):
    def handle_item(self, context: LoaderContext, item: str):
        assert(type(item) == str)
        context.imports[context.current_filename].append(item)
