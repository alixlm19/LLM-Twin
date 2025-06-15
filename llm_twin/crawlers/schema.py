from typing import TypedDict


class DriverOptions(TypedDict):
    args: list[str]
    kwargs: dict[str, str | int]


class DriverSettings(TypedDict):
    name: str
    options: DriverOptions
