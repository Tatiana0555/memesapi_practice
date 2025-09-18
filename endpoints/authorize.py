import requests
import allure
from endpoints.endpoint import Endpoint


class Authorize(Endpoint):
    url = f'{Endpoint.base_url}/authorize'

    @allure.step('Authorize user with name={name}')
    def get_token(self, name: str):
        self.response = requests.post(self.url, json={"name": name})
        self.json = self.response.json()
        return self.json['token']

    @allure.step('Check token is alive')
    def check_token_alive(self, token: str):
        url = f'{self.url}/{token}'
        self.response = requests.get(url)
        return self.response.status_code == 200
