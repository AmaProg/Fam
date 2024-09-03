from pytest import fixture


@fixture
def login_command() -> list[str]:
    return ["login"]


@fixture
def signup_command() -> list[str]:
    return ["signup"]
