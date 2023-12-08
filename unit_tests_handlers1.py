import unittest
from fastapi.testclient import TestClient
from main import get_application


class BattleSavesTests(unittest.TestCase):
    def setUp(self):
        self.app = get_application()
        self.client = TestClient(self.app)

    def test_search(self):
        print('test_search')
        response = self.client.get('/api/search?name_to_find="mega"')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        response_data = response.json()
        print(response_data)
        for item in response_data:
            self.assertTrue('mega' in item['name'], f"Expected 'mega' in {item['name']}")

if __name__ == '__main__':
    unittest.main()
