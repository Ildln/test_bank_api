from src.main.api.models.base_model import BaseModel


class CreditRepayRequest(BaseModel):
    creditId: int
    accountId: int
    amount: float


class CreditRepayResponse(BaseModel):
    creditId: int
    amountDeposited: float