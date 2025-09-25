import requests
from endpoints.endpoint import Endpoint
import allure

class MemesClient(Endpoint):

    @allure.step("Create meme")
    def create(self, body: dict):
        resp = requests.post(f"{self.base_url}/meme", json=body, headers=self.headers)
        self.check_status_code(resp, 200)
        return resp

    @allure.step("Get meme by id={meme_id}")
    def get(self, meme_id: int):
        resp = requests.get(f"{self.base_url}/meme/{meme_id}", headers=self.headers)
        self.check_status_code(resp, 200)
        return resp

    @allure.step("Update meme id={meme_id}")
    def update(self, meme_id: int, body: dict):
        resp = requests.put(f"{self.base_url}/meme/{meme_id}", json=body, headers=self.headers)
        self.check_status_code(resp, 200)
        return resp

    @allure.step("Delete meme id={meme_id}")
    def delete(self, meme_id: int):
        resp = requests.delete(f"{self.base_url}/meme/{meme_id}", headers=self.headers)
        return resp
