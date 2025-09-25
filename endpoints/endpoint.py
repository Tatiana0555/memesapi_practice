import allure


class Endpoint:
    base_url = "http://memesapi.course.qa-practice.com"
    response = None
    json = None
    headers = {}


    @allure.step('Check that response status is {status_code}')
    def check_status_code(self, response, status_code: int):
        """Проверка статуса ответа."""
        assert response.status_code == status_code, \
            f"Expected {status_code}, got {response.status_code}"

    @allure.step('Check that field "{field}" equals "{value}"')
    def check_field_equals(self, response, field: str, value):
        """Проверка поля JSON ответа."""
        json_data = response.json()
        assert json_data.get(field) == value, \
            f"Expected {field}={value}, got {json_data.get(field)}"
