import requests

from src.main.api.models.auth.login import LoginRequest, LoginResponse



class RequestSpecs:
    @staticmethod
    def base_headers():
        return {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    @staticmethod
    def auth_headers(username: str, password: str):
        login_request = LoginRequest(username=username, password=password)
        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_request.model_dump(),
            headers=RequestSpecs.base_headers()
        )
        if response.status_code == 200:
            response_data = LoginResponse(**response.json())
            token = response_data.token
            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return headers
        raise Exception("Failed to login")

    @staticmethod
    def admin_auth_headers():
        return RequestSpecs.auth_headers(username="admin", password="123456")

    @staticmethod
    def unauth_headers():
        return RequestSpecs.base_headers()