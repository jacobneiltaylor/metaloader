import dataclasses

from typing import Dict, List
from collections import defaultdict


def _field(factory):
    return dataclasses.field(default_factory=factory)


@dataclasses.dataclass
class LoaderContext:
    imports: Dict[str, List[str]] = _field(lambda: defaultdict(list))
    filenames: List[str] = _field(list)
    data: dict = _field(dict)
    import_count: int = 0

    @property
    def current_filename(self):
        return self.filenames[self.import_count]
