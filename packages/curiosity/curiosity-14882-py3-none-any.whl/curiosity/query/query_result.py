from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, List

from .. import EmittedNode


@dataclass
class QueryResults:
    R: Dict[str, List[EmittedNode]]
    C: Dict[str, int]

    MS: float

    @property
    def elapesd(self) -> timedelta:
        return timedelta(milliseconds=self.MS)

    def get_emitted(self, emit_key: str) -> List[EmittedNode]:
        return self.R[emit_key]

    def get_emitted_count(self, emit_key: str) -> int:
        return self.C[emit_key]
