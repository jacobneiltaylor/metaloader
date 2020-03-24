import os
from .filesystem import Filesystem


class LocalFilesystem(Filesystem, register="local"):
    def __init__(self, root: str = None):
        super().__init__()
        if not root:
            root = os.getcwd()
        self._root = root

    def get_filename(self, *args):
        return os.path.join(self._root, *args)

    def _open(self, filename: str):
        return open(filename, "rb")

    def exists(self, filename: str):
        return os.path.isfile(filename)
