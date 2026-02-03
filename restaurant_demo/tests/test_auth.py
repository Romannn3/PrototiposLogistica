import pytest
from app.models import Usuario


def test_login_page_loads(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Iniciar' in response.data or b'Ingresar' in response.data


def test_login_with_valid_credentials(client, app):
    response = client.post('/auth/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Bienvenido' in response.data or b'Dashboard' in response.data


def test_login_with_invalid_credentials(client):
    response = client.post('/auth/login', data={
        'username': 'admin',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    
    assert b'incorrectos' in response.data or b'error' in response.data.lower()


def test_logout(authenticated_client):
    response = authenticated_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert 'login' in response.request.path.lower() or 'Sesión cerrada'.encode('utf-8') in response.data


def test_protected_route_without_auth(client):
    response = client.get('/', follow_redirects=False)
    assert response.status_code == 302
    assert '/auth/login' in response.location
