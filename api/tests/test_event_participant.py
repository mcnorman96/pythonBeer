import unittest
from models.event_participant import EventParticipant

class TestEventParticipantModel(unittest.TestCase):
    def test_create(self):
        ep = EventParticipant(id=1, event_id=2, user_id=3)
        self.assertEqual(ep.id, 1)
        self.assertEqual(ep.event_id, 2)
        self.assertEqual(ep.user_id, 3)

if __name__ == '__main__':
    unittest.main()
