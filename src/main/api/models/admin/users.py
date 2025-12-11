from typing import List
from pydantic import RootModel
from src.main.api.models.base_model import BaseModel


class AdminUser(BaseModel):
    id: int
    username: str
    role: str

class AdminUsersResponse(RootModel[List[AdminUser]]):
    ...