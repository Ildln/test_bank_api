from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.admin.create_user import CreateCreditUserRequest
from src.main.api.models.credits.repay import CreditRepayRequest
from src.main.api.models.credits.request import CreditRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.admin.create_user import CreateUserRequest


class CreditUserSteps(BaseSteps):
    def credit_request(self, create_credit_user_req: CreateCreditUserRequest, credit_request: CreditRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_credit_user_req.username, password=create_credit_user_req.password),
            endpoint=Endpoint.CREDIT_REQUEST,
            response_spec=ResponseSpecs.status_created(),
        ).post(credit_request)
        return response

    def credit_invalid_request(self, create_credit_user_req: CreateCreditUserRequest, credit_request: CreditRequest):
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_credit_user_req.username, password=create_credit_user_req.password),
            endpoint=Endpoint.CREDIT_REQUEST,
            response_spec=ResponseSpecs.status_bad()
        ).post(credit_request)
        return response

    def credit_request_forbidden_role(self, create_user_req: CreateUserRequest, credit_request: CreditRequest):
        response= CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_req.username, password=create_user_req.password),
            endpoint=Endpoint.CREDIT_REQUEST,
            response_spec=ResponseSpecs.status_forbidden(),
        ).post(credit_request)
        return response

    def credit_repay(self, create_credit_user_req: CreateCreditUserRequest, credit_repay_request: CreditRepayRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_credit_user_req.username, password=create_credit_user_req.password),
            endpoint=Endpoint.CREDIT_REPAY,
            response_spec=ResponseSpecs.status_ok(),
        ).post(credit_repay_request)
        return response

    def credit_repay_invalid_partial_amount(self, create_credit_user_req: CreateCreditUserRequest, credit_repay_request: CreditRepayRequest):
        return CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_credit_user_req.username, password=create_credit_user_req.password),
            endpoint=Endpoint.CREDIT_REPAY,
            response_spec=ResponseSpecs.status_unprocessable(),
        ).post(credit_repay_request)

    def credit_request_second_credit_not_found(self, create_credit_user_req: CreateCreditUserRequest, credit_request: CreditRequest):
        return CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_credit_user_req.username, password=create_credit_user_req.password),
            endpoint=Endpoint.CREDIT_REQUEST,
            response_spec=ResponseSpecs.status_not_found(),
        ).post(credit_request)

    def credit_history(self, create_credit_user_request: CreateCreditUserRequest):
        return ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
            endpoint=Endpoint.CREDIT_HISTORY,
            response_spec=ResponseSpecs.status_ok()
        ).get()