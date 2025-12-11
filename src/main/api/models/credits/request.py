from src.main.api.models.base_model import BaseModel


class CreditRequest(BaseModel):
    accountId: int
    amount: float
    termMonths: int


class CreditResponse(BaseModel):
    id: int
    amount: float
    termMonths: int
    balance: float
    creditId: int