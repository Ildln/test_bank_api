from dataclasses import dataclass


@dataclass(frozen=True)
class ProductInfo:
    name: str
    price: float