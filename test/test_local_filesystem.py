import mock
from os.path import join, dirname, abspath
from metaloader import Serialisation
from integration_test import IntegrationTest


def mock_cwd(root):
    retval = join(dirname(abspath(__file__)), "data", root)
    return mock.patch("os.getcwd", mock.MagicMock(return_value=retval))


def run_local_fs_test(serialisation_str):
    serialisation = None
    if serialisation != "json":
        serialisation = Serialisation.get(serialisation_str)
    test = IntegrationTest(None, serialisation, serialisation_str)
    test.run()


@mock_cwd("json")
def test_json_local_fs():
    run_local_fs_test("json")


@mock_cwd("yaml")
def test_yaml_local_fs():
    run_local_fs_test("yaml")
