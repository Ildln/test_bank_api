from src.main.api.models.base_model import BaseModel
from typing import List, Optional


class Transaction(BaseModel):
    transactionId: int
    type: str
    amount: float
    fromAccountId: Optional[int]
    toAccountId: Optional[int]
    createdAt: str
    creditId: Optional[int]

class AccountTransactionsResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: List[Transaction]