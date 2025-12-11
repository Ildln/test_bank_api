from typing import Optional
from src.main.api.models.base_model import BaseModel
from typing import Protocol
from requests import Response


class CrudEndpoint(Protocol):
    def post(self, model: Optional[BaseModel] = None) -> BaseModel | Response:...
    def get(self, id: Optional[int] = None) -> BaseModel | Response:...
    def delete(self, user_id: int) -> BaseModel | Response:...
