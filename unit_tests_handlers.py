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

    def test_pagination(self):
        print('test_pagination')
        response = self.client.get('/api/pagination?offset=0&limit=20')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')

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


if __name__ == '__main__':
    unittest.main()
