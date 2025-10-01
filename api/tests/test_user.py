from models.user import User
from app import app
from werkzeug.exceptions import Unauthorized
import pytest

def test_create_user():
    user = User(id=1, username='testuser', password='secret', email='test@example.com')
    assert user.id == 1
    assert user.username == 'testuser'
    assert user.password == 'secret'
    assert user.email == 'test@example.com'

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

## Register Tests
def test_register_success(client, mocker):
    mock_user = mocker.Mock()
    mock_user.id = 123
    mocker.patch('routes.auth.UserService.create', return_value=mock_user)
    response = client.post('/auth/register', json={
        'username': 'newuser',
        'password': 'password',
        'email': 'newuser@example.com'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered'
    assert response.get_json()['user_id'] == 123

def test_register_missing_fields(client, mocker):
    mocker.patch('routes.auth.UserService.create', side_effect=ValueError('Missing fields'))
    response = client.post('/auth/register', json={
        'username': 'newuser'
        # missing password and email
    })
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_register_internal_error(client, mocker):
    mocker.patch('routes.auth.UserService.create', side_effect=Exception('DB error'))
    response = client.post('/auth/register', json={
        'username': 'newuser',
        'password': 'password',
        'email': 'newuser@example.com'
    })
    assert response.status_code == 500
    assert 'error' in response.get_json()

## LOGOUT TESTS
def test_logout_success(client):
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    response = client.post('/auth/logout')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Logged out successfully!'


## LOGIN TESTS
def test_login_success(client, mocker):
    mock_user = mocker.Mock()
    mock_user.id = 1
    mock_user.password = 'hashed_pw'
    mock_user.username = 'user'
    mock_user.email = 'user@example.com'
    mock_user.to_dict.return_value = {
        'id': 1,
        'username': 'user',
        'email': 'user@example.com'
    }

    mock_query = mocker.Mock()
    mock_filter = mocker.Mock()
    mock_filter.first.return_value = mock_user
    mock_query.filter_by.return_value = mock_filter
    mocker.patch('routes.auth.db.session.query', return_value=mock_query)
    mocker.patch('routes.auth.check_password_hash', return_value=True)  # <-- Add this line

    response = client.post('/auth/login', json={'username': 'user', 'password': 'hashed_pw'})
    assert response.status_code == 200
    assert 'token' in response.get_json()

def test_login_missing_fields(client):
    response = client.post('/auth/login', json={'username': 'user'})
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_login_incorrect_credentials(client, mocker):
    mocker.patch('routes.auth.db.session.query', return_value=mocker.Mock(filter_by=lambda **kwargs: mocker.Mock(first=lambda: None)))
    response = client.post('/auth/login', json={'username': 'user', 'password': 'wrong'})
    assert response.status_code == 401
    assert 'error' in response.get_json()

def test_login_internal_error(client, mocker):
    mocker.patch('routes.auth.db.session.query', side_effect=Exception('DB error'))
    response = client.post('/auth/login', json={'username': 'user', 'password': 'pass'})
    assert response.status_code == 500
    assert 'error' in response.get_json()