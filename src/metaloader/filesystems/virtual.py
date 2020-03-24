from io import BytesIO
from .filesystem import Filesystem
from ..serialisations import Serialisation


class VirtualFilesystem(Filesystem, register="virtual"):
    """
        Represents a virtual filesystem, used for testing
    """

    def __init__(self, data: dict, serialisation: str):
        super().__init__()
        self._data = {}
        self._serialisation = Serialisation.get(serialisation)

        for key, value in data.items():
            args = self._serialisation.decode_import(key)
            filename = self.get_filename(*args)
            self._data[filename] = value

    def get_filename(self, *args):
        path = "/".join(args)
        return f"/{path}"

    def _open(self, filename):
        filestream = BytesIO()
        return self._serialisation.serialise(self._data[filename], filestream)

    def exists(self, filename):
        return filename in self._data
