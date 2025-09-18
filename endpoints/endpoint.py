import allure


class Endpoint:
    base_url = 'http://memesapi.course.qa-practice.com'
    response = None
    json = None
    headers = {}

    @allure.step('Check that response status is {status_code}')
    def check_status_code(self, status_code: int):
        assert self.response.status_code == status_code, \
            f"Expected {status_code}, got {self.response.status_code}"

    @allure.step('Check that field "{field}" equals "{value}"')
    def check_field_equals(self, field: str, value):
        assert self.json.get(field) == value, \
            f"Expected {field}={value}, got {self.json.get(field)}"
