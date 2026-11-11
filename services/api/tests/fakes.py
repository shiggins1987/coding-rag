class FakeReady:
    def __init__(self, ok: bool = True) -> None:
        self.ok = ok

    def ready(self) -> bool:
        return self.ok