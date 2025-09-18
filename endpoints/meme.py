import requests
import allure
from endpoints.endpoint import Endpoint

class Meme(Endpoint):
    url = f'{Endpoint.base_url}/meme'

    @allure.step('Get all memes')
    def get_all_memes(self):
        self.response = requests.get(self.url, headers=self.headers)
        try:
            self.json = self.response.json()
        except ValueError:
            self.json = None
        return self.response

    @allure.step('Get meme by id')
    def get_meme(self, meme_id: int):
        self.response = requests.get(f'{self.url}/{meme_id}', headers=self.headers)
        try:
            self.json = self.response.json()
        except ValueError:
            self.json = None
        return self.response

    @allure.step('Create new meme')
    def create_meme(self, body: dict):
        self.response = requests.post(self.url, json=body, headers=self.headers)
        self.json = self.response.json()
        return self.json['id']

    @allure.step('Update meme by id')
    def update_meme(self, meme_id: int, body: dict):
        self.response = requests.put(f'{self.url}/{meme_id}', json=body, headers=self.headers)
        self.json = self.response.json()
        return self.response

    @allure.step('Delete meme by id')
    def delete_meme(self, meme_id: int):
        self.response = requests.delete(f'{self.url}/{meme_id}', headers=self.headers)
        return self.response
