from typing import Protocol

class Ready(Protocol):
    def read(self) -> bool: ...