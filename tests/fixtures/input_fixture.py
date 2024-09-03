from pytest import fixture

from tests.utils import input_value


@fixture
def user_login_input(user_login) -> str:

    email, pwd = user_login

    return input_value([email, pwd])
