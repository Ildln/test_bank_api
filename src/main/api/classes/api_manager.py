from typing import List, Any

from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.credit_user_steps import CreditUserSteps
from src.main.api.steps.user_steps import UserSteps


class ApiManager:
    def __init__(self, created_obj: List[Any]):
        self.admin_steps = AdminSteps(created_obj)
        self.user_steps = UserSteps(created_obj)
        self.credit_user_steps = CreditUserSteps(created_obj)