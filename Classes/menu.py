from dataclasses import dataclass


@dataclass(frozen=True)
class MenuItem:
    name: str
    price: int
    image_link: str
    description: str


