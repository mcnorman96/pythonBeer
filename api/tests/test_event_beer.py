import unittest
from models.event_beer import EventBeer
from datetime import datetime

class TestEventBeerModel(unittest.TestCase):
    def test_to_dict(self):
        added_at = datetime(2024, 1, 1, 12, 0)
        eb = EventBeer(id=1, event_id=2, beer_id=3, added_at=added_at)
        expected = {
            'id': 1,
            'event_id': 2,
            'beer_id': 3,
            'added_at': added_at,
        }
        self.assertEqual(eb.to_dict(), expected)

if __name__ == '__main__':
    unittest.main()
