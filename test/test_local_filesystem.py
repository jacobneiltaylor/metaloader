from os.path import join, dirname, abspath

from metaloader import Filesystem, Serialisation

from integration_test import IntegrationTest


def get_local_fs(root):
    return Filesystem.get("local", root=root)


def run_local_fs_test(serialisation_str):
    root = join(dirname(abspath(__file__)), "data", serialisation_str)
    fs = get_local_fs(root)
    serialisation = Serialisation.get(serialisation_str)
    test = IntegrationTest(fs, serialisation, serialisation_str)
    test.run()


def test_json_local_fs():
    run_local_fs_test("json")


def test_yaml_local_fs():
    run_local_fs_test("yaml")
