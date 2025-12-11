from src.main.api.models.base_model import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str



class User(BaseModel):
    username: str
    role: str

class LoginResponse(BaseModel):
    token: str
    user: User