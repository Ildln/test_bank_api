import pytest

from src.main.api.models.credits.request import CreditRequest


@pytest.fixture
def credit_request_factory(api_manager, credit_account_factory, create_credit_user_request):
    def _make_credit(amount: int):
        account = credit_account_factory()
        credit_req = CreditRequest(accountId=account.id, amount=amount, termMonths=12)
        response = api_manager.credit_user_steps.credit_request(create_credit_user_request, credit_req)
        assert credit_req.accountId == response.id
        return response

    return _make_credit