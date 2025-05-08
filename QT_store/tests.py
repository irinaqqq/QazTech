import unittest
import requests

class TestGraphicsAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://20.121.43.134:8000/api/graphics/"
        self.headers = {
            "accept": "application/json",
            "X-CSRFTOKEN": "1SKvru3GoZ2hnm8Z4oQff0gb21uZiGURlxDCOyGoAjof0QTqicWEd2uOa6PR7Yrs"
        }

    def test_get_graphics(self):
        response = requests.get(self.base_url, headers=self.headers)
        # Проверка, что ответ успешный
        self.assertEqual(response.status_code, 200, f"Expected 200 OK, got {response.status_code}")

        # Проверка, что приходит JSON
        self.assertEqual(response.headers["Content-Type"], "application/json", "Expected application/json response")

        # Проверка, что данные приходят в виде списка (если API возвращает список графиков)
        data = response.json()
        self.assertIsInstance(data, list, "Expected response data to be a list")

if __name__ == "__main__":
    unittest.main()
