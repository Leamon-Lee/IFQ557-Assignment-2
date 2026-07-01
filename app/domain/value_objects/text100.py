from dataclasses import dataclass


@dataclass(frozen=True)
class Text100:
    value: str

    def __post_init__(self) -> None:
        if self.value is None:
            raise ValueError("Text100 cannot be None")
        if len(self.value) > 100:
            raise ValueError("Text100 cannot be longer than 100 characters")

    def __str__(self) -> str:
        return self.value
