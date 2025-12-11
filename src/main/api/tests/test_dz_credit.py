import pytest

from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.models.credits.repay import CreditRepayRequest
from src.main.api.models.credits.request import CreditRequest



class TestCredit:
    def test_user_credit_request_valid(self, api_manager, credit_account_factory, create_credit_user_request):
        """Тест на запрос на получение кредите /credit/request"""

        # Создаем Банковский счет.
        account1 = credit_account_factory()

        # создаем запрос на получение кредита
        credit_request = CreditRequest(accountId=account1.id, amount=15000, termMonths=12)
        response = api_manager.credit_user_steps.credit_request(create_credit_user_request, credit_request)

        assert credit_request.amount == response.amount
        assert credit_request.accountId == response.id

        # Get
        check_history = api_manager.credit_user_steps.credit_history(create_credit_user_request)
        assert check_history.credits[0].creditId == response.creditId
        assert check_history.credits[0].amount == credit_request.amount


    @pytest.mark.parametrize("summa", [4999, 15001])
    def test_user_credit_request_invalid(self, api_manager, credit_account_factory, create_credit_user_request, summa):
        """Негативный Тест на запрос на получение кредита /credit/request. Валидный диапазон 5000-15000"""
        # Создаем Банковский счет
        account = credit_account_factory()

        # создаем запрос на получение кредита
        credit_request = CreditRequest(accountId=account.id, amount=summa, termMonths=12)
        response = api_manager.credit_user_steps.credit_invalid_request(create_credit_user_request, credit_request)

        assert response.json()["error"] == "Amount must be between 5000 and 15000"

    def test_credit_request_forbidden_role(self, api_manager, create_user_request, account_factory):
        """Негативный Тест на получение кредита с использованием невалидной ролью пользователя "ROLE_USER" """
        account = account_factory()   # Создаем счет в банке с ролью - "ROLE_USER"

        # Делаем запрос на получение кредита с ролью "ROLE_USER"
        credit_request = CreditRequest(accountId=account.id, amount=6000, termMonths=12)
        response = api_manager.credit_user_steps.credit_request_forbidden_role(create_user_request, credit_request)

        assert response.json()["detail"] == "Forbidden: ROLE_CREDIT access required"

    def test_credit_request_second_credit_not_found(self, api_manager, create_credit_user_request, credit_account_factory):
        """Негативный тест: Берем кредит на второй счет, при уже активном первом """
        account1 = credit_account_factory()
        account2 = credit_account_factory()
        credit_request = CreditRequest(accountId=account1.id, amount=6000, termMonths=12)
        api_manager.credit_user_steps.credit_request(create_credit_user_request, credit_request)

        credit_request = CreditRequest(accountId=account2.id, amount=6000, termMonths=12)
        response = api_manager.credit_user_steps.credit_request_second_credit_not_found(create_credit_user_request, credit_request)
        assert response.json()["error"] == "Only one active credit allowed per user", response.text



    def test_user_credit_repay(self, api_manager, create_credit_user_request, credit_request_factory):
        """Тест на проверку погашения кредита /credit/reapy
        - кредит можно погасить только один раз, и на всю сумму
        """
        credit = credit_request_factory(amount=6000)

        # Гасим кредит один платежом
        credit_repay_request = CreditRepayRequest(creditId=credit.creditId, accountId=credit.id, amount=credit.amount)
        response = api_manager.credit_user_steps.credit_repay(create_credit_user_request, credit_repay_request)

        assert credit_repay_request.amount == response.amountDeposited
        assert response.creditId == credit_repay_request.creditId

        # Get
        check_history = api_manager.credit_user_steps.credit_history(create_credit_user_request)
        assert check_history.credits[0].creditId == response.creditId
        assert check_history.credits[0].amount == response.amountDeposited

    def test_credit_repay_partial_amount(self, api_manager, create_credit_user_request, credit_request_factory):
        """Негативный тест: "Гасим кредит не на всю сумму" """
        credit_response = credit_request_factory(amount=10000)
        credit_repay_req = CreditRepayRequest(creditId=credit_response.creditId, accountId=credit_response.id, amount=5000)
        response = api_manager.credit_user_steps.credit_repay_invalid_partial_amount(create_credit_user_request, credit_repay_req)

        assert response.json()["error"] == f"The amount is not enough. Credit balance: {int(0 - credit_response.amount)}"

    def test_credit_repay_amount_exceeds_balance(self, api_manager, create_credit_user_request, credit_request_factory):
        """Негативный тест: "Сумма погашения кредита превышает саму сумму кредита" """
        credit_response = credit_request_factory(amount=5000)
        credit_repay_req = CreditRepayRequest(creditId=credit_response.creditId, accountId=credit_response.id, amount=7000)
        response = api_manager.credit_user_steps.credit_repay_invalid_partial_amount(create_credit_user_request, credit_repay_req)

        assert response.json()["error"] == f"Insufficient funds. Current balance: {credit_response.amount:.2f}, required: {credit_repay_req.amount:.2f}"

    def test_credit_repay_twice_invalid(self, api_manager, create_credit_user_request, credit_request_factory):
        """Негативный тест: "Повторно гасим кредит, который уже погасили" """
        credit_response = credit_request_factory(amount=5000)
        credit_repay_req = CreditRepayRequest(creditId=credit_response.creditId, accountId=credit_response.id, amount=5000)
        api_manager.credit_user_steps.credit_repay(create_credit_user_request, credit_repay_req)

        response = api_manager.credit_user_steps.credit_repay_invalid_partial_amount(create_credit_user_request, credit_repay_req)

        assert response.json()["error"] == f"Insufficient funds. Current balance: 0.00, required: {credit_repay_req.amount:.2f}"