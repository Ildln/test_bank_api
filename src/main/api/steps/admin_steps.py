from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.admin.create_user import CreateUserRequest
from src.main.api.models.auth.login import LoginRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.requesters.crud_requester import CrudRequester


class AdminSteps(BaseSteps):
    def create_user(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.admin_auth_headers(),
            endpoint=Endpoint.ADMIN_CREATE_USER,
            response_spec=ResponseSpecs.status_ok(),
        ).post(create_user_request)

        self.created_obj.append(response)
        return response

    def delete_user(self, user_id: int):
        CrudRequester(
            request_spec=RequestSpecs.admin_auth_headers(),
            endpoint=Endpoint.ADMIN_DELETE_USER,
            response_spec=ResponseSpecs.status_ok(),
        ).delete(user_id)

    def create_user_invalid(self, create_user_request: CreateUserRequest):
        CrudRequester(
            request_spec=RequestSpecs.admin_auth_headers(),
            endpoint=Endpoint.ADMIN_CREATE_USER,
            response_spec=ResponseSpecs.status_bad()
        ).post(create_user_request)

    def login_user(self, login_request: LoginRequest):
        return ValidateCrudRequester(
            request_spec=RequestSpecs.unauth_headers(),
            endpoint=Endpoint.LOGIN_USER,
            response_spec=ResponseSpecs.status_ok()
        ).post(login_request)

    def admin_users(self):
        return ValidateCrudRequester(
            request_spec=RequestSpecs.admin_auth_headers(),
            endpoint=Endpoint.ADMIN_USERS,
            response_spec=ResponseSpecs.status_ok()
        ).get()