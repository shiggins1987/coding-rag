from typing import Protocol

class Ready(Protocol):
    def ready(self) -> bool: ...