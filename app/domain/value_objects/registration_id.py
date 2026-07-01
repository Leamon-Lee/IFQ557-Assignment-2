from dataclasses import dataclass


@dataclass(frozen=True)
class RegistrationId:
    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise TypeError("RegistrationId must be an integer")
        if self.value <= 0:
            raise ValueError("RegistrationId must be greater than 0")

    def __int__(self) -> int:
        return self.value
