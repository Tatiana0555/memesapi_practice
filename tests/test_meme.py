import pytest
import requests
from endpoints.memes import MemesClient

@pytest.fixture
def memes_client(auth_headers):
    client = MemesClient()
    client.headers = auth_headers
    return client


@pytest.fixture
def created_meme(memes_client):
    """Создаёт мем перед тестом и удаляет после."""
    body = {
        "text": "pytest meme",
        "url": "https://example.com/test.png",
        "tags": ["test", "pytest"],
        "info": {"created_by": "pytest"}
    }
    resp = memes_client.create(body)
    meme = resp.json()
    meme_id = meme["id"]
    yield meme
    memes_client.delete(meme_id)


def test_create_meme_returns_valid_data(memes_client):
    body = {
        "text": "pytest meme",
        "url": "https://example.com/test.png",
        "tags": ["test", "pytest"],
        "info": {"created_by": "pytest"}
    }
    resp = memes_client.create(body)
    memes_client.check_field_equals(resp, "text", body["text"])
    memes_client.check_field_equals(resp, "url", body["url"])
    memes_client.check_field_equals(resp, "tags", body["tags"])
    memes_client.check_field_equals(resp, "info", body["info"])
    memes_client.delete(resp.json()["id"])


def test_get_meme_returns_expected_data(memes_client, created_meme):
    meme_id = created_meme["id"]
    resp = memes_client.get(meme_id)
    memes_client.check_field_equals(resp, "id", meme_id)
    memes_client.check_field_equals(resp, "text", created_meme["text"])
    memes_client.check_field_equals(resp, "url", created_meme["url"])
    memes_client.check_field_equals(resp, "tags", created_meme["tags"])
    memes_client.check_field_equals(resp, "info", created_meme["info"])


def test_update_meme_changes_fields(memes_client, created_meme):
    meme_id = created_meme["id"]
    body = {
        "id": meme_id,
        "text": "updated meme",
        "url": "https://example.com/updated.png",
        "tags": ["updated", "pytest"],
        "info": {"updated_by": "pytest"}
    }
    memes_client.update(meme_id, body)
    resp = memes_client.get(meme_id)
    memes_client.check_field_equals(resp, "text", body["text"])
    memes_client.check_field_equals(resp, "url", body["url"])
    memes_client.check_field_equals(resp, "tags", body["tags"])
    memes_client.check_field_equals(resp, "info", body["info"])


def test_delete_meme_removes_resource(memes_client, created_meme):
    meme_id = created_meme["id"]
    resp = memes_client.delete(meme_id)
    assert resp.status_code == 200

    resp = requests.get(f"{memes_client.base_url}/meme/{meme_id}", headers=memes_client.headers)
    assert resp.status_code == 404


@pytest.mark.parametrize("body", [
    {"text": "", "url": "https://example.com/test.png", "tags": [], "info": {}},
    {"text": "test", "url": "", "tags": ["tag"], "info": {"info": 1}},
    {},
])
def test_create_meme_invalid_data_returns_error(memes_client, body):
    resp = requests.post(
        f"{memes_client.base_url}/meme",
        json=body,
        headers=memes_client.headers
    )
    assert resp.status_code == 400
