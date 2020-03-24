import mock
from os.path import join, dirname, abspath
from metaloader import Filesystem, Serialisation
from integration_test import IntegrationTest


def get_absolute_root(root):
    return join(dirname(abspath(__file__)), "data", root)


def mock_cwd(root):
    retval = get_absolute_root(root)
    return mock.patch("os.getcwd", mock.MagicMock(return_value=retval))


def run_local_fs_test(serialisation_str):
    serialisation = None
    fs = None

    if serialisation_str != "json":
        serialisation = Serialisation.get(serialisation_str)
    else:
        fs = Filesystem.get("local", get_absolute_root("json"))

    test = IntegrationTest(fs, serialisation, serialisation_str)
    test.run()

    if fs:
        assert "root.json" in fs.history[0]


def test_json_local_fs():
    run_local_fs_test("json")


@mock_cwd("yaml")
def test_yaml_local_fs():
    run_local_fs_test("yaml")
