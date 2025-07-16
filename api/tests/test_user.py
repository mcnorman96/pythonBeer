from models.user import User

def test_create_user():
    user = User(id=1, username='testuser', password='secret', email='test@example.com')
    assert user.id == 1
    assert user.username == 'testuser'
    assert user.password == 'secret'
    assert user.email == 'test@example.com'
