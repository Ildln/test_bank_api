import pytest

from src.main.api.generators.model_generator import RandomModelGeneration
from src.main.api.models.accounts.deposit import DepositRequest



class TestApiAccount:
    def test_create_account(self, api_manager, create_user_request):
        """Тест на создание одного аккаунта"""
        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0

        # Проверяем через метод GET
        check_transactions = api_manager.user_steps.account_transactions(create_user_request, response.id)
        assert check_transactions.id == response.id
        assert check_transactions.number == response.number
        assert check_transactions.balance == response.balance

    def test_create_third_account_limit_reached(self, api_manager, create_user_request):
        """Негативный тест на создание 3-х банковских счетов у одного пользователя"""
        api_manager.user_steps.create_account(create_user_request)
        api_manager.user_steps.create_account(create_user_request)
        response = api_manager.user_steps.create_account_exceeds_limit(create_user_request)

        assert response.json()["error"] == "User already has maximum number of accounts(2)"



    def test_account_deposit_valid(self, api_manager, create_user_request, account_):
        """Тест на пополнение банковского счета /deposit"""
        # Пополняем счет
        deposit_request = RandomModelGeneration.generate(DepositRequest)
        deposit_request.accountId = account_.id
        response = api_manager.user_steps.account_deposit(create_user_request, deposit_request)

        assert deposit_request.accountId == response.id
        assert response.balance == deposit_request.amount

        # Проверяем через метод GET
        check_transactions = api_manager.user_steps.account_transactions(create_user_request, response.id)
        assert check_transactions.id == response.id
        assert check_transactions.number ==  account_.number
        assert check_transactions.balance == response.balance

    @pytest.mark.parametrize("balance",[999, 9001, 0, -1])
    def test_account_deposit_invalid(self, balance, api_manager, account_, create_user_request):
        """
        Негативный тест на пополнение банковского счета. Валидный диапазон: 1000 - 9000
        """
        account_deposit_request = DepositRequest(accountId=account_.id, amount=balance)
        api_manager.user_steps.account_deposit_invalid(create_user_request, account_deposit_request)

