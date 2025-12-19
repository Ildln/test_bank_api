import pytest

from src.main.api.models.accounts.transfer import AccountTransferRequest


@pytest.mark.api
class TransferApiAccount:
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


    @pytest.mark.parametrize("deposit, transfer" ,[(3000, 499), (9000, 10001)])
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