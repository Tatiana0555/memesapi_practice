import requests
from endpoints.meme import Meme
from endpoints.authorize import Authorize


def test_create_and_delete_meme(meme_endpoint, meme_body):
    meme_id = meme_endpoint.create_meme(meme_body)
    meme_endpoint.check_status_code(200)
    meme_endpoint.delete_meme(meme_id)
    meme_endpoint.check_status_code(200)


def test_update_meme(meme_endpoint, meme_body):
    meme_id = meme_endpoint.create_meme(meme_body)
    meme_endpoint.check_status_code(200)
    updated_body = meme_body.copy()
    updated_body.update({
        "id": meme_id,
        "text": "Updated meme text",
        "tags": ["funny", "updated"],
        "url": "https://images.chesscomfiles.com/uploads/v1/blog/640393.672c38ed.668x375o.1e02a635934e@2x.jpeg",
        "info": {"cat": "loading"}
    })
    meme_endpoint.update_meme(meme_id, updated_body)
    meme_endpoint.check_status_code(200)
    meme_endpoint.delete_meme(meme_id)
    meme_endpoint.check_status_code(200)


def test_get_all_memes(meme_endpoint):
    meme_endpoint.get_all_memes()
    meme_endpoint.check_status_code(200)


def test_invalid_token():
    m = Meme()
    m.headers = {"Authorization": "wrongtoken"}
    m.get_all_memes()
    assert m.response.status_code == 401


def test_get_meme_by_id(meme_endpoint, meme_body):
    meme_id = meme_endpoint.create_meme(meme_body)
    meme_endpoint.check_status_code(200)

    meme_endpoint.get_meme(meme_id)
    meme_endpoint.check_status_code(200)
    meme_endpoint.check_field_equals('text', meme_body['text'])

    meme_endpoint.delete_meme(meme_id)
    meme_endpoint.check_status_code(200)

#
# def test_update_meme_partial_data(meme_endpoint, meme_body):
#     meme_id = meme_endpoint.create_meme(meme_body)
#     meme_endpoint.check_status_code(200)
#
#     updated_body = {"text": "Updated partial meme text"}
#     meme_endpoint.update_meme(meme_id, updated_body)
#     meme_endpoint.check_status_code(200)
#
#     meme_endpoint.delete_meme(meme_id)
#     meme_endpoint.check_status_code(200)


def test_delete_nonexistent_meme(meme_endpoint):
    nonexistent_meme_id = 999999999
    meme_endpoint.delete_meme(nonexistent_meme_id)
    meme_endpoint.check_status_code(404)


def test_create_meme_invalid_data(meme_endpoint):
    invalid_body = {
        "url": "https://example.com/meme.jpg",
        "tags": ["funny", "new"]
    }  # Отсутствует обязательное поле "text"

    meme_endpoint.response = requests.post(meme_endpoint.url, json=invalid_body, headers=meme_endpoint.headers)
    meme_endpoint.check_status_code(400)  # Ожидаем ошибку валидации

#
# def test_access_rights(meme_endpoint, meme_body, auth_token):
#     meme_id = meme_endpoint.create_meme(meme_body)
#     meme_endpoint.check_status_code(200)
#
#     # Создаем второго пользователя с другим токеном
#     another_auth = Authorize()
#     another_token = another_auth.get_token("AnotherUser")
#
#     another_meme_endpoint = Meme()
#     another_meme_endpoint.headers = {"Authorization": another_token}
#
#     # Пробуем получить мем первого пользователя с токеном второго пользователя
#     another_meme_endpoint.get_meme(meme_id)
#     another_meme_endpoint.check_status_code(403)  # Ожидаем ошибку доступа
#
#     meme_endpoint.delete_meme(meme_id)
#     meme_endpoint.check_status_code(200)

def test_meme_access_rights(meme_endpoint, meme_body, auth_token):
    # Создаем мем с первым пользователем
    meme_id = meme_endpoint.create_meme(meme_body)
    meme_endpoint.check_status_code(200)

    # Создаем второго пользователя с другим токеном
    another_auth = Authorize()
    another_token = another_auth.get_token("AnotherUser")

    another_meme_endpoint = Meme()
    another_meme_endpoint.headers = {"Authorization": another_token}

    # Пробуем получить мем первого пользователя с токеном второго пользователя
    another_meme_endpoint.get_meme(meme_id)
    another_meme_endpoint.check_status_code(200)  # Мем доступен для чтения

    # Пробуем удалить мем первого пользователя с токеном второго пользователя
    another_meme_endpoint.delete_meme(meme_id)
    another_meme_endpoint.check_status_code(403)  # Ожидаем ошибку доступа

    # Удаляем мем первым пользователем
    meme_endpoint.delete_meme(meme_id)
    meme_endpoint.check_status_code(200)

