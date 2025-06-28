import unittest
from models.user import User

class TestUserModel(unittest.TestCase):
    def test_create(self):
        user = User(id=1, username='testuser', password='secret', email='test@example.com')
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.password, 'secret')
        self.assertEqual(user.email, 'test@example.com')

if __name__ == '__main__':
    unittest.main()
