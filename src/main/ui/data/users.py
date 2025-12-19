from dataclasses import dataclass



@dataclass(frozen=True)
class UserCredConfiguration:
    username: str
    password: str = "secret_sauce"

class UsersCred:
    STANDARD = UserCredConfiguration(username="standard_user")

    LOCKED_OUT = UserCredConfiguration(username="locked_out_user")

    VISUAL = UserCredConfiguration(username="visual_user")