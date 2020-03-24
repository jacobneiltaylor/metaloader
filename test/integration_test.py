import pytest

from metaloader import (
    FlatLoader,
    ExclusiveStanzaClashError
)
from schema import SCHEMA_PASS, SCHEMA_FAIL_EXCLUSIVE

MSG = "Cannot have more than one 'example_dict' stanza"


class IntegrationTest:
    def __init__(self, fs, serialisation, file_ext=None):
        self.fs = fs
        self.serialisation = serialisation
        self.file_ext = file_ext

    def _get_root_filename(self):
        if self.file_ext:
            return f"root.{self.file_ext}"
        return "root"

    def _get_base_loader(self, schema):
        loader = FlatLoader(serialisation=self.serialisation)
        loader.set_schema(schema)
        return loader

    def _test_pass(self):
        loader = self._get_base_loader(SCHEMA_PASS)
        context = loader.load(self._get_root_filename(), self.fs)

        assert context.import_count == 4

    def _test_fail(self):
        loader = self._get_base_loader(SCHEMA_FAIL_EXCLUSIVE)

        with pytest.raises(ExclusiveStanzaClashError) as excinfo:
            loader.load(self._get_root_filename(), self.fs)

        assert MSG in str(excinfo.value)

    def run(self):
        self._test_pass()
