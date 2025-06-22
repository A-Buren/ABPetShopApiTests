from http.client import responses
import allure
import jsonschema
import pytest
import requests

from .conftest import create_pet
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

            with allure.step("Проверка статуса ответа"):
                assert response.status_code == 200, "Статус ответа не совпал с ожидаемым"

            with allure.step("Проверка текстового содержимого ответа"):
                assert response.text == 'Pet deleted', "Текст ответа не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(f"{BASE_URL}/pet", json=payload)
            with allure.step("Проверка статуса ответа"):
                assert response.status_code == 404, "Статус ответа не совпал с ожидаемым"

            with allure.step("Проверка текстового содержимого ответа"):
                assert response.text == 'Pet not found', "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить несуществующего питомца")
    def test_getting_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение несуществующего питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

            with allure.step("Проверка статуса ответа"):
                assert response.status_code == 404, "Статус ответа не совпал с ожидаемым"

            with allure.step("Проверка текстового содержимого ответа"):
                assert response.text == 'Pet not found'

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "Имя питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "Статус питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца с полными данными")
    def test_add_pet_full_data(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": [
                    "string"
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ],
                "status": "available"
            }

        with allure.step("Отправка запроса на добавление нового питомца с полными данными"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

            with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
                assert response.status_code == 200, "Статус ответа не совпадает с ожидаемым"
                jsonschema.validate(response_json, PET_SCHEMA)

            with allure.step("Проверка параметров питомца в ответа"):
                assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
                assert response_json['name'] == payload['name'], "Имя питомца не совпадает с ожидаемым"
                assert response_json['category']['id'] == payload['category'][
                    'id'], "id категории питомца не совпадает с ожидаемым"
                assert response_json['category']['name'] == payload['category'][
                    'name'], "имя категории питомца не совпадает с ожидаемым"
                assert response_json['photoUrls'] == payload['photoUrls']
                assert response_json['tags'][0]['id'] == payload['tags'][0]['id'], "tags id не совпадает с ожидаемым"
                assert response_json['tags'][0]['name'] == payload['tags'][0][
                    'name'], "tags name не совпадает с ожидаемым"
                assert response_json['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet['id']

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            assert response.json()['id'] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_info_about_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet['id']

        with allure.step("Подготовка данных для обновления питомца"):
            payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }
        with allure.step('Отправка запроса на обновление информации о питомце по ID'):
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
            assert response_json['id'] == payload['id'], f"Expected {payload['id']}, but got {response_json['id']}"
            assert response_json['name'] == payload[
                'name'], f"Expected {payload['name']}, but got {response_json['name']}"
            assert response_json['status'] == payload[
                'status'], f"Expected {payload['status']}, but got {response_json['status']}"

    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet['id']

        with allure.step('Отправка запроса на удаление питомца по ID'):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 404, f"Expected 400, but got {response.status_code}"

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("available", 200),
            ("pending", 200),
            ("sold", 200),
            ("blablabla", 400),
            ("", 400)
        ]
    )
    def test_get_pet_by_status(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомца по статусу {status}"):
            response = requests.get(url=f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == expected_status_code, f"Expected {expected_status_code}, but got {response.status_code}"

        if expected_status_code == 200:
            with allure.step("Проверяем формат данных"):
                assert isinstance(response.json(), list)

        else:
            with allure.step("Проверяем формат ошибки"):
                assert isinstance(response.json(), dict)

