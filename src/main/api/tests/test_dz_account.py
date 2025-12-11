import pytest

from src.main.api.generators.model_generator import RandomModelGeneration
from src.main.api.models.accounts.deposit import DepositRequest
from src.main.api.models.accounts.transfer import AccountTransferRequest



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



    def test_account_transfer_valid(self, api_manager, account_factory, create_user_request):
        """Тест: перевод средст между банковскими счетами /transfer"""
        account1 = account_factory(balance=2000)
        account2 = account_factory()

        # Делаем перевод между счетами
        account_transfer_request = AccountTransferRequest(fromAccountId=account1.id, toAccountId=account2.id, amount=500)
        response = api_manager.user_steps.account_transfer(create_user_request, account_transfer_request)

        assert response.fromAccountIdBalance == 1500

        # Проверяем через метод GET 1 - account
        check_transactions_acc1 = api_manager.user_steps.account_transactions(create_user_request, response.fromAccountId)
        assert check_transactions_acc1.id == response.fromAccountId
        assert check_transactions_acc1.balance == response.fromAccountIdBalance

        # Проверяем через метод GET 2 - account 
        check_transactions_acc2 = api_manager.user_steps.account_transactions(create_user_request, response.toAccountId)
        assert check_transactions_acc2.id == response.toAccountId
        assert check_transactions_acc2.number == account2.number


    @pytest.mark.parametrize("deposit, transfer",[(3000, 499), (9000, 10001)])
    def test_account_transfer_invalid_amount(self, deposit, transfer, api_manager, account_factory, create_user_request):
        """НЕГАТИВНЫЙ Тест: перевод средст между банковскими счетами /transfer"""
        account1 = account_factory(balance=deposit)
        account2 = account_factory()

        # Делаем перевод между счетами
        account_transfer_request = AccountTransferRequest(fromAccountId=account1.id, toAccountId=account2.id, amount=transfer)
        response = api_manager.user_steps.account_transfer_invalid_amount(create_user_request, account_transfer_request)

        assert "Amount must be between 500 and 10000" in response.text

    def test_account_transfer_insufficient_funds(self, api_manager, account_factory, create_user_request):
        """Негативный тест - "Недостаточно средств для перевода". """
        account1 = account_factory(balance=3000)
        account2 = account_factory()

        account_transfer_request = AccountTransferRequest(fromAccountId=account1.id, toAccountId=account2.id, amount=5000)
        response = api_manager.user_steps.account_transfer_insufficient_funds(create_user_request, account_transfer_request)

        assert "Insufficient funds." in response.json()["error"]
        assert response.json()["error"] == f"Insufficient funds. Current balance: {account1.balance:.2f}, required: {account_transfer_request.amount:.2f}"