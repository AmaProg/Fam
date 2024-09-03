from pytest import fixture


@fixture
def login_command() -> list[str]:
    return ["login"]
