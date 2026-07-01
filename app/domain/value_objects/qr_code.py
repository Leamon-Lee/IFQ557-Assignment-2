from dataclasses import dataclass


@dataclass(frozen=True)
class QRCode:
    value: str

    def __post_init__(self) -> None:
        if not 1 <= len(self.value) <= 255:
            raise ValueError("QR code must be 1 to 255 characters")
        if any(char.isspace() for char in self.value):
            raise ValueError("QR code cannot contain spaces")
        if any(ord(char) > 127 for char in self.value):
            raise ValueError("QR code must contain ASCII characters only")

    def __str__(self) -> str:
        return self.value
