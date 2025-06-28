import unittest
from models.rating import Rating

class TestRatingModel(unittest.TestCase):
    def test_to_dict(self):
        rating = Rating(id=1, event_id=2, beer_id=3, user_id=4, taste=5, aftertaste=6, smell=7, design=8, score=9)
        expected = {
            'id': 1,
            'event_id': 2,
            'beer_id': 3,
            'user_id': 4,
            'taste': 5,
            'aftertaste': 6,
            'smell': 7,
            'design': 8,
            'score': 9
        }
        self.assertEqual(rating.to_dict(), expected)

if __name__ == '__main__':
    unittest.main()
