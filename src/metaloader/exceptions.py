_CLASH_ERR = "Cannot have more than one '{}' stanza (Clashing files: {})"
_VALID_ERR = "The data in the '{}' stanza from '{}' failed validation rules."


class MetaloaderError(RuntimeError):
    pass


class ExclusiveStanzaClashError(MetaloaderError):
    def __init__(self, key, clashing_files):
        error_message = _CLASH_ERR.format(key, clashing_files)
        super().__init__(error_message)


class StanzaValidationError(MetaloaderError):
    def __init__(self, key, filename):
        error_message = _VALID_ERR.format(key, filename)
        super().__init__(error_message)
