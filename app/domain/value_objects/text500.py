from dataclasses import dataclass


@dataclass(frozen=True)
class Text500:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Text500 cannot be empty")
        if len(self.value) > 500:
            raise ValueError("Text500 cannot be longer than 500 characters")
        if self.value.strip() != self.value:
            raise ValueError("Text500 cannot start or end with spaces")

    def __str__(self) -> str:
        return self.value
