from dataclasses import dataclass


@dataclass(frozen=True)
class EventTitle:
    value: str

    def __post_init__(self) -> None:
        if not 1 <= len(self.value) <= 100:
            raise ValueError("Event title must be 1 to 100 characters")
        if self.value.strip() != self.value:
            raise ValueError("Event title cannot start or end with spaces")

    def __getitem__(self, key):
        return self.value[key]

    def __len__(self) -> int:
        return len(self.value)

    def __str__(self) -> str:
        return self.value
