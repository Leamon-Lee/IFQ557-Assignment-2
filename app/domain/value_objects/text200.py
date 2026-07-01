from dataclasses import dataclass


@dataclass(frozen=True)
class Text200:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) > 200:
            raise ValueError("Text200 cannot be longer than 200 characters")

    def __str__(self) -> str:
        return self.value
