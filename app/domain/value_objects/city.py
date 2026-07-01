from dataclasses import dataclass


@dataclass(frozen=True)
class City:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("City cannot be empty")

    def __str__(self) -> str:
        return self.value
