_CLASH_ERR = "Cannot have more than one '{}' stanza (Clashing files: {})"


class MetaloaderError(RuntimeError):
    pass


class ExclusiveStanzaClashError(MetaloaderError):
    def __init__(self, key, clashing_files):
        error_message = _CLASH_ERR.format(key, clashing_files)
        super().__init__(error_message)
