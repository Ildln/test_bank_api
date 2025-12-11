from dataclasses import dataclass
from typing import Optional, Union

Number = Union[int, float]

@dataclass
class CreationRule:
    regex: Optional[str] = None
    min_value: Optional[Number] = None
    max_value: Optional[Number] = None