from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type
from pydantic import RootModel

from src.main.api.models.accounts.transactions import AccountTransactionsResponse
from src.main.api.models.admin.users import AdminUsersResponse
from src.main.api.models.base_model import BaseModel
from src.main.api.models.accounts.deposit import DepositRequest, DepositResponse
from src.main.api.models.accounts.transfer import AccountTransferRequest, AccountTransferResponse
from src.main.api.models.accounts.create_response import CreateAccountResponse
from src.main.api.models.credits.history import CreditHistoryResponse
from src.main.api.models.admin.create_user import CreateUserRequest, CreateUserResponse
from src.main.api.models.credits.repay import CreditRepayRequest, CreditRepayResponse
from src.main.api.models.auth.login import LoginRequest, LoginResponse
from src.main.api.models.credits.request import CreditRequest, CreditResponse



@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]] | None
    response_model: Optional[Type[BaseModel]] | type[RootModel] | None


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model=CreateUserRequest,
        url="/admin/create",
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        url="/admin/users",
        request_model=None,
        response_model=None
    )

    LOGIN_USER = EndpointConfiguration(
        request_model=LoginRequest,
        url="/auth/token/login",
        response_model=LoginResponse
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model=None,
        url="/account/create",
        response_model=CreateAccountResponse,
    )

    ACCOUNT_DEPOSIT = EndpointConfiguration(
        request_model=DepositRequest,
        url="/account/deposit",
        response_model=DepositResponse,
    )

    ACCOUNT_TRANSFER = EndpointConfiguration(
        request_model=AccountTransferRequest,
        url="/account/transfer",
        response_model=AccountTransferResponse,
    )

    CREDIT_REQUEST = EndpointConfiguration(
        request_model=CreditRequest,
        url="/credit/request",
        response_model=CreditResponse,
    )

    CREDIT_REPAY = EndpointConfiguration(
        request_model=CreditRepayRequest,
        url="/credit/repay",
        response_model=CreditRepayResponse,
    )

    ACCOUNT_TRANSACTIONS = EndpointConfiguration(
        request_model=None,
        url="/account/transactions",
        response_model=AccountTransactionsResponse
    )

    CREDIT_HISTORY = EndpointConfiguration(
        request_model=None,
        url="/credit/history",
        response_model=CreditHistoryResponse
    )

    ADMIN_USERS = EndpointConfiguration(
        request_model=None,
        url="/admin/users",
        response_model=AdminUsersResponse
    )