from http.client import responses

import requests
import allure
import pytest
import jsonschema
from .schemas.store_schema import STORE_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    @allure.title('Размещение заказа')
    def test_placing_order(self):
        with allure.step("Подготовка данных для отправки запроса"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()
            with allure.step("Проверка статуса ответа"):
                assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

            with allure.step("Проверка формата данных в ответе"):
                assert response_json['id'] == payload['id'], f"Expected {payload['id']}, but got {response_json['id']}"
                assert response_json['petId'] == payload[
                    'petId'], f"Expected {payload['petId']}, but got {response_json['petId']}"
                assert response_json['quantity'] == payload[
                    'quantity'], f"Expected {payload['quantity']}, but got {response_json['quantity']}"
                assert response_json['status'] == payload[
                    'status'], f"Expected {payload['status']}, but got {response_json['status']}"
                assert response_json['complete'] == payload[
                    'complete'], f"Expected {payload['complete']}, but got {response_json['complete']}"

    @allure.title('Получение информации о заказе по ID')
    def test_get_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order['id']

        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            response_json = response.json()

            with allure.step("Проверка статуса ответа"):
                assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

            with allure.step("Проверка данных в ответе"):
                assert response_json['id'] == create_order['id'], f"Expected create_order['id'], but got {response_json['id']}"
                assert response_json['petId'] == create_order['petId'], f"Expected create_order['petId'], but got {response_json['petId']}"
                assert response_json['quantity'] == create_order['quantity'], f"Expected response_json['quantity'], but got {response_json['quantity']}"
                assert response_json['status'] == create_order['status'], f"Expected response_json['status'], but got {response_json['status']}"
                assert response_json['complete'] == create_order['complete'], f"Expected response_json['complete'], but got {response_json['complete']}"

    @allure.title('Удаление заказа по ID')
    def test_delete_order_by_id(self,create_order):
        with allure.step('Получение ID заказа'):
            order_id = create_order['id']

        with allure.step('Отправка запроса на удаление заказа'):
            response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

        with allure.step('Отправка запроса на получение информации о заказе по ID '):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 404, f"Expected 404, but got {response.status_code}"

    @allure.title('Попытка получить информацию о несуществующем заказе')
    def test_getting_nonexistent_order(self):
        with allure.step("Отправка запроса на получение несуществующего заказа"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, f"Expected 404,but got {response.status_code}"

    @allure.title('Получение инвентаря магазина')
    def test_getting_inventory_of_store(self):
        with allure.step('Отправка запроса на получение инвентаря магазина'):
            response = requests.get(url=f"{BASE_URL}/store/inventory")

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

        with allure.step('Проверка формата ответа'):
            response_json = response.json()
            assert "approved" in response_json, "Параметр 'approved' отсутствует в ответе"
            assert isinstance(response_json['approved'], int), "Параметр 'approved' должен быть целым числом"
            assert "delivered" in response_json, "Параметр 'delivered' отсутствует в ответе"
            assert isinstance(response_json['delivered'], int), "Параметр 'delivered' должен быть целым числом"