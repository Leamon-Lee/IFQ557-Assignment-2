from dataclasses import dataclass


@dataclass(frozen=True)
class OrganizationName:
    value: str

    def __post_init__(self) -> None:
        if not 1 <= len(self.value) <= 120:
            raise ValueError("Organization name must be 1 to 120 characters")
        if self.value.strip() != self.value:
            raise ValueError("Organization name cannot start or end with spaces")

    def __str__(self) -> str:
        return self.value
