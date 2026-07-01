from dataclasses import dataclass


@dataclass(frozen=True)
class VenueName:
    value: str


@dataclass(frozen=True)
class Address:
    value: str


@dataclass(frozen=True)
class City:
    value: str


@dataclass(frozen=True)
class Room:
    value: str
