import pytest

from src.main.api.models.auth.login import LoginRequest



@pytest.mark.api
class TestUserLogin:
    def test_admin_login(self, api_manager):
        admin_login_request = LoginRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(admin_login_request)

        assert admin_login_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

    def test_user_login(self, api_manager, create_user_request):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username
        assert response.user.role == "ROLE_USER"