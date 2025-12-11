import pytest

from src.main.api.models.accounts.deposit import DepositRequest


@pytest.fixture
def account_(api_manager, create_user_request):
    response = api_manager.user_steps.create_account(create_user_request)
    return response

@pytest.fixture
def account_factory(api_manager, create_user_request):
    def _create_account(balance: int = 0):
        response = api_manager.user_steps.create_account(create_user_request)
        if balance:
            response = api_manager.user_steps.account_deposit(create_user_request, DepositRequest(accountId=response.id, amount=balance))
        return response
    return _create_account

@pytest.fixture
def credit_account_factory(api_manager, create_credit_user_request):
    def _create_account(balance: int = 0):
        response = api_manager.user_steps.create_account(create_credit_user_request)
        if balance:
            response = api_manager.user_steps.account_deposit(create_credit_user_request, DepositRequest(accountId=response.id, amount=balance))
        return response
    return _create_account