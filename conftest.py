import pytest
from endpoints.authorize import Authorize
from endpoints.meme import Meme


@pytest.fixture(scope='session')
def auth_token():
    auth = Authorize()
    token = auth.get_token("TestUser")
    return token


@pytest.fixture()
def meme_endpoint(auth_token):
    meme = Meme()
    meme.headers = {"Authorization": auth_token}
    return meme


@pytest.fixture()
def meme_body():
    return {
        "text": "Funny meme",
        "url": "http://example.com/meme.jpg",
        "tags": ["funny", "new"],
        "info": {"author": "me"}
    }
