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

    def test_pagination(self):
        print('test_pagination')
        response = self.client.get('/api/pagination?offset=0&limit=20')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        response_data = response.json()
        # print(response_data)
        for item in response_data:
            self.assertTrue('name' in item.keys(), "Expected 'name' in response")
            self.assertTrue('height' in item.keys(), "Expected 'height' in response")
            self.assertTrue('hp' in item.keys(), "Expected 'hp' in response")
            self.assertTrue('attack' in item.keys(), "Expected 'attack' in response")
            self.assertTrue('defence' in item.keys(), "Expected 'defence' in response")
            self.assertTrue('speed' in item.keys(), "Expected 'speed' in response")
            self.assertTrue('picture' in item.keys(), "Expected 'picture' in response")
            self.assertTrue('choose' in item.keys(), "Expected 'choose' in response")

    def test_save_battle_round(self):
        print('test_save_battle_round')
        user = {
            'user_pokemon': 'user_pokemon',
            'computer_pokemon': 'computer_pokemon',
            'data': '2023-01-01',
            'winner': 'asd'}
        response = self.client.post('/api/save_battle_round', json=user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')

    def test_save_pokemon_to_ftp(self):
        pokemonData = {
            'name': 'asd',
            'height': 2,
            'hp': 3,
            'attack': 4,
            'defence': 5,
            'speed': 6,
            'picture': 'asd'
        }
        print('test_save_pokemon_to_ftp')
        response = self.client.post('/api/save_pokemon_to_ftp', json=pokemonData)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')

    def test_get_all_battle_saves(self):
        response = self.client.get('/api/get_all_battle_saves')
        print(response)
        print('test_get_all_battle_saves')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        response_data = response.json()
        # print(response_data)
        for item in response_data:
            self.assertTrue('id' in item.keys(), "Expected 'name' in response")
            self.assertTrue('data' in item.keys(), "Expected 'height' in response")
            self.assertTrue('date_of_round' in item.keys(), "Expected 'hp' in response")
            self.assertTrue('user_pokemon' in item.keys(), "Expected 'attack' in response")
            self.assertTrue('computer_pokemon' in item.keys(), "Expected 'defence' in response")
            self.assertTrue('winner' in item.keys(), "Expected 'speed' in response")

if __name__ == '__main__':
    unittest.main()
