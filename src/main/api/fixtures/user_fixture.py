import pytest

from src.main.api.generators.model_generator import RandomModelGeneration
from src.main.api.models.admin.create_user import CreateUserRequest, CreateCreditUserRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGeneration.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_credit_user_request(api_manager):
    credit_user_req = RandomModelGeneration.generate(CreateCreditUserRequest)
    api_manager.admin_steps.create_user(credit_user_req)
    return credit_user_req