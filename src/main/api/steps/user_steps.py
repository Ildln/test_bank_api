from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.accounts.deposit import DepositRequest
from src.main.api.models.accounts.transfer import AccountTransferRequest
from src.main.api.models.admin.create_user import CreateUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.requesters.crud_requester import CrudRequester


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            endpoint=Endpoint.CREATE_ACCOUNT,
            response_spec=ResponseSpecs.status_created()
        ).post()
        return response

    def create_account_exceeds_limit(self, create_user_request: CreateUserRequest):
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            endpoint=Endpoint.CREATE_ACCOUNT,
            response_spec=ResponseSpecs.status_conflict()
        ).post()
        return response

    def account_deposit(self, create_user_request: CreateUserRequest, account_deposit_request: DepositRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            endpoint=Endpoint.ACCOUNT_DEPOSIT,
            response_spec=ResponseSpecs.status_ok()
        ).post(account_deposit_request)
        return response

    def account_deposit_invalid(self, create_user_request: CreateUserRequest, account_deposit_request: DepositRequest):
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            endpoint=Endpoint.ACCOUNT_DEPOSIT,
            response_spec=ResponseSpecs.status_bad()
        ).post(account_deposit_request)


    def account_transfer(self, create_user_request: CreateUserRequest, account_transfer_request: AccountTransferRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            endpoint=Endpoint.ACCOUNT_TRANSFER,
            response_spec=ResponseSpecs.status_ok()
        ).post(account_transfer_request)
        return response

    def account_transfer_invalid_amount(self, create_user_request: CreateUserRequest, account_transfer_request: AccountTransferRequest):
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            endpoint=Endpoint.ACCOUNT_TRANSFER,
            response_spec=ResponseSpecs.status_bad()
        ).post(account_transfer_request)
        return response

    def account_transfer_insufficient_funds(self, create_user_request: CreateUserRequest, account_transfer_request: AccountTransferRequest):
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            endpoint=Endpoint.ACCOUNT_TRANSFER,
            response_spec=ResponseSpecs.status_unprocessable()
        ).post(account_transfer_request)
        return response

    def account_transactions(self, create_user_request: CreateUserRequest, account_id: int):
        return ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            endpoint=Endpoint.ACCOUNT_TRANSACTIONS,
            response_spec=ResponseSpecs.status_ok()
        ).get(account_id)





