import pytest

from metaloader import (
    FlatLoader,
    ExclusiveStanzaClashError
)
from schema import SCHEMA_PASS, SCHEMA_FAIL_EXCLUSIVE

ERR_MSG_EXCLUSIVE = "Cannot have more than one 'test_dict' stanza"
NONEXIST_FILENAME = "dummy.nonexistent.file"
TEST_DATA = tuple(range(1, 13))

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

        print(context)

        assert tuple(context.data["test_list"]) == TEST_DATA

        for i in TEST_DATA:
            assert str(i) in context.data["test_dict"]
            assert context.data["test_dict"][str(i)] == str(i)

    def _test_fail_exclusive(self):
        loader = self._get_base_loader(SCHEMA_FAIL_EXCLUSIVE)

        with pytest.raises(ExclusiveStanzaClashError) as excinfo:
            loader.load(self._get_root_filename(), self.fs)

        assert ERR_MSG_EXCLUSIVE in str(excinfo.value)

    def _test_fail_nonexist(self):
        loader = self._get_base_loader(SCHEMA_FAIL_EXCLUSIVE)

        with pytest.raises(FileNotFoundError) as excinfo:
            loader.load(NONEXIST_FILENAME, self.fs)

        assert NONEXIST_FILENAME in str(excinfo.value)

    def run(self):
        self._test_pass()
        self._test_fail_exclusive()
        self._test_fail_nonexist()
