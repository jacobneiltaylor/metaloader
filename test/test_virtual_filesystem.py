import metaloader
from integration_test import IntegrationTest

VFS_DATA = {
    "root": {
        "$imports": ["import_1", "import_3"],
        "test_list": [1, 2, 3],
        "test_dict": {
            "4": "4",
            "5": "5",
            "6": "6"
        },
        "test_exclusive": {
            "hello": "world"
        }
    },

    "import_1": {
        "$imports": ["folder.import_2"],
        "test_list": [4, 5, 6],
        "test_dict": {
            "1": "1",
            "2": "2",
            "3": "3"
        }
    },

    "folder.import_2": {
        "test_list": [7, 8, 9],
        "test_dict": {
            "10": "10",
            "11": "11",
            "12": "12"
        }
    },

    "import_3": {
        "test_list": [10, 11, 12],
        "test_dict": {
            "7": "7",
            "8": "8",
            "9": "9"
        }
    },

    "validation_fail": {
        "test_list": {}
    }
}


def test_all_serialisations():
    for serialisation_str in metaloader.Serialisation.registry.enum():
        serialisation = metaloader.Serialisation.get(serialisation_str)
        fs = metaloader.Filesystem.get("virtual", VFS_DATA, serialisation_str)
        test = IntegrationTest(fs, serialisation, serialisation.EXTENSION)
        test.run()
