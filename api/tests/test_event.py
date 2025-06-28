import unittest
from models.event import Event
from datetime import datetime

class TestEventModel(unittest.TestCase):
    def test_to_dict(self):
        start = datetime(2024, 1, 1, 12, 0)
        end = datetime(2024, 1, 2, 12, 0)
        event = Event(id=1, name='Party', start_date=start, end_date=end, description='Fun')
        expected = {
            'id': 1,
            'name': 'Party',
            'start_date': start.isoformat(),
            'end_date': end.isoformat(),
            'description': 'Fun',
        }
        self.assertEqual(event.to_dict(), expected)

if __name__ == '__main__':
    unittest.main()
