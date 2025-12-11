from typing import Annotated

from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel


class DepositRequest(BaseModel):
    accountId: int
    amount: Annotated[float, CreationRule(min_value=1000, max_value=9000)]


class DepositResponse(BaseModel):
    id: int
    balance: float