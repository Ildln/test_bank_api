import requests
import allure

from typing import Optional
from requests import Response
from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel

class CrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel] = None) -> Response:
        body = model.model_dump() if model is not None else ""

        with allure.step(f"POST {Config.fetch("backendUrl")}{self.endpoint.value.url}"):
            allure.attach(str(body), "Request body", allure.attachment_type.JSON)

        response = requests.post(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}",
            headers=self.request_spec,
            json=body,
        )

        allure.attach(
            response.text,
            "Response body",
            allure.attachment_type.JSON
        )

        self.response_spec(response)
        return response

    def delete(self, user_id: int):
        response = requests.delete(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}/{user_id}",
            headers=self.request_spec
        )
        self.response_spec(response)
        return response

    def get(self, id: Optional[int] = None) -> Response:
        base_url = f"{Config.fetch('backendUrl')}{self.endpoint.value.url}"
        url = f"{base_url}/{id}" if id is not None else base_url
        response = requests.get(
            url = url,
            headers=self.request_spec
        )
        self.response_spec(response)
        return response