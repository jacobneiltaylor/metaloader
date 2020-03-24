SCHEMA_PASS = {
    "test_list": "list",
    "test_dict": "dict",
    "test_exclusive": {
        "name": "dict",
        "exclusive": True
    }
}

SCHEMA_FAIL_EXCLUSIVE = {
    "test_list": "list",
    "test_dict": {
        "name": "dict",
        "exclusive": True
    },
    "test_exclusive": {
        "name": "dict",
        "exclusive": True
    }
}
