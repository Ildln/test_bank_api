import allure
import pytest

from src.main.ui.data.messages import Message
from src.main.ui.data.users import UsersCred

pytestmark = [pytest.mark.ui, allure.epic("Saucedemo"), allure.feature("Auth")]

from src.main.ui.pages.login_page import LoginPage

@allure.title("Авторизация: standard_user успешно входит в систему")
def test_auth(page):
    (
        LoginPage(page)
        .open()
        .login_success(UsersCred.STANDARD)
    )

@allure.title("Авторизация: locked_out_user — показывается ошибка и логин не выполняется")
def test_auth_locked_out_user(page):
    (
        LoginPage(page).open().login_fail(UsersCred.LOCKED_OUT)
        .should_have_url("https://www.saucedemo.com/")
        .should_have_error(Message.LOCKED_OUT_ERROR)
    )

def test_logout(page):
    (
        LoginPage(page).open().login_success(UsersCred.STANDARD)
        .should_be_opened()
        .logout()
        .should_have_url("https://www.saucedemo.com/")
    )

def test_visual_user_logout(page):
    (
        LoginPage(page).open().login_success(UsersCred.VISUAL)
        .should_be_opened()
        .logout()
        .should_have_url("https://www.saucedemo.com/")
    )
