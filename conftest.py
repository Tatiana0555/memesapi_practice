import pytest
from endpoints.authorize import Authorize

NAME = "test_user"


@pytest.fixture(scope="session")
def auth_token():
    """Токен авторизации на всю сессию pytest."""
    auth = Authorize()
    token = auth.get_token(NAME)
    if not auth.check_token_alive(token):
        token = auth.get_token(NAME)
    return token


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    """Заголовки с токеном для клиентов API."""
    return {"Authorization": auth_token}
