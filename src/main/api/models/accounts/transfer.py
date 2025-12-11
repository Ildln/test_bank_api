from src.main.api.models.base_model import BaseModel


class AccountTransferRequest(BaseModel):
    fromAccountId: int
    toAccountId: int
    amount: float


class AccountTransferResponse(BaseModel):
    fromAccountId: int
    toAccountId: int
    fromAccountIdBalance: float
