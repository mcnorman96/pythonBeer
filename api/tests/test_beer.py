import unittest
from models.beer import Beer

class TestBeerModel(unittest.TestCase):
    def test_to_dict(self):
        beer = Beer(id=1, name='Test', description='Desc', brewery='Brew', type='Lager')
        expected = {
            'id': 1,
            'name': 'Test',
            'description': 'Desc',
            'brewery': 'Brew',
            'type': 'Lager'
        }
        self.assertEqual(beer.to_dict(), expected)

if __name__ == '__main__':
    unittest.main()
