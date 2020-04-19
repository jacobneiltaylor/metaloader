import re
from copy import copy
from collections import deque

from .exceptions import StanzaValidationError
from .stanzahandlers import StanzaHandler
from .loader_context import LoaderContext
from .serialisations import Serialisation
from .filesystems import Filesystem
from .directives import Directive

DEFAULT_LOADER_WHITELIST = (
    "imports",
)


class FlatLoader:
    _DIRECTIVE_RGX = re.compile(r"\$.+")

    def __init__(
            self,
            serialisation: Serialisation = None,
            directives: tuple = DEFAULT_LOADER_WHITELIST
    ):
        if not serialisation:
            serialisation = Serialisation.get("json")

        self._serialisation = serialisation
        self._stanza_handlers = {}
        self._directives = {name: Directive.get(name) for name in directives}

    def register_handler(self, stanza_handler: StanzaHandler):
        self._stanza_handlers[stanza_handler.key] = stanza_handler

    def set_schema(self, schema: dict):
        self._stanza_handlers = {}
        for key, value in schema.items():
            if isinstance(value, dict):
                value["key"] = key
                handler = StanzaHandler.get(**value)
            else:
                handler = StanzaHandler.get(value, key)

            self.register_handler(handler)

    def _load_file(self, fs: Filesystem, filename: str) -> dict:
        with fs.open(filename) as filestream:
            return self._serialisation.deserialise(filestream)

    def _process_directives(self, ctx: LoaderContext, data: dict) -> dict:
        doc_directives = {
            key: value for key, value in data.items()
            if self._DIRECTIVE_RGX.match(key)
        }

        for key, value in doc_directives.items():
            del data[key]
            key = key[1:]
            if key in self._directives:
                self._directives[key].handle_directive(ctx, value)

        return data

    def _cleanup_handlers(self):
        for handler in self._stanza_handlers.values():
            handler.cleanup()

    def load(self, root_filename: str, fs: Filesystem = None) -> LoaderContext:
        if not fs:
            fs = Filesystem.get("local")

        root_filename = fs.canonicalise(root_filename)
        ctx = LoaderContext()

        stack = deque()
        stack.append(root_filename)

        while stack:
            filename = stack.pop()
            directory = fs.get_dir_name(filename)

            ctx.filenames.append(filename)

            data = self._process_directives(ctx, self._load_file(fs, filename))

            new_imports = copy(ctx.imports[filename])
            new_imports.reverse()

            for new_import in new_imports:
                decoded_import = self._serialisation.decode_import(new_import)
                stack.append(fs.get_filename(decoded_import, directory))

            for key, stanzadata in data.items():
                if key in self._stanza_handlers:
                    handler = self._stanza_handlers[key]

                    if handler.is_valid(stanzadata):
                        handler.include(ctx, stanzadata)
                    else:
                        raise StanzaValidationError(key, filename)

            ctx.import_count += 1
        ctx.imports = dict(ctx.imports)
        self._cleanup_handlers()
        return ctx
