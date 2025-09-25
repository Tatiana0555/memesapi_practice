import requests
from endpoints.endpoint import Endpoint
import allure

class Authorize(Endpoint):
    url = f"{Endpoint.base_url}/authorize"

    @allure.step("Authorize user with name={name}")
    def get_token(self, name: str):
        """Получение нового токена."""
        resp = requests.post(self.url, json={"name": name})
        resp.raise_for_status()
        return resp.json()["token"]

    @allure.step("Check if token is alive")
    def check_token_alive(self, token: str):
        """Проверка жив ли токен."""
        resp = requests.get(f"{self.url}/{token}")
        return resp.status_code == 200
