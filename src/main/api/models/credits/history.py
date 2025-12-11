from src.main.api.models.base_model import BaseModel
from typing import List


class CreditHistory(BaseModel):
    creditId: int
    accountId: int
    amount: float
    termMonths: int
    balance: float
    createdAt: str

class CreditHistoryResponse(BaseModel):
    userId: int
    credits: List[CreditHistory]