import pytest

from src.main.api.generators.model_generator import RandomModelGeneration
from src.main.api.models.admin.create_user import CreateUserRequest


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGeneration.generate(CreateUserRequest)]
    )
    def test_create_user_valid(self, api_manager, create_user_request):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        # GET
        check_users = api_manager.admin_steps.admin_users()
        assert check_users.root[1].id == response.id
        assert check_users.root[1].username == response.username
        assert check_users.root[1].role == response.role

        created_user = next(u for u in check_users.root if u.id == response.id)
        assert created_user.username == response.username


    @pytest.mark.parametrize(
        "username, password", [
            ("абв", "Pas!sw0rd"),
            ("Ma", "Pas!sw0rd"),
            ("qwertyuiopasdf16", "Pas!sw0rd"),
            ("Max#", "Pas!sw0rd"),
            ("Max301", "пассворL#11"),
            ("Max302", "Pas!sw0"),
            ("Max303", "pas!sw0rd"),
            ("Max304", "PAS!SW0RD"),
            ("Max305", "Passsw0rd"),
            ("Max306", "Pas!sword")]
    )
    def test_create_user_invalid(self, username, password, api_manager):
        base_user = RandomModelGeneration.generate(CreateUserRequest)
        create_user_req = base_user.model_copy(update={"username": username, "password": password})

        api_manager.admin_steps.create_user_invalid(create_user_req)