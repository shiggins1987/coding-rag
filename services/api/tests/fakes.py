class FakeReady:
    def __init__(self, ok: bool = True) -> None:
        self.ok = ok

    def read(self) -> bool:
        return self.ok