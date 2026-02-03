import pytest

def test_login_page(client):
    response = client.get('/auth/login')
    assert response.status_code == 200

def test_login_with_valid_credentials(client):
    response = client.post('/auth/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
    assert response.status_code == 200

def test_dashboard_shows_alerts(authenticated_client, app):
    response = authenticated_client.get('/')
    assert response.status_code == 200
    assert b'Dashboard' in response.data or b'Pedidos' in response.data

def test_pedidos_list(authenticated_client):
    response = authenticated_client.get('/pedidos/')
    assert response.status_code == 200

def test_crear_desde_mensaje_page(authenticated_client):
    response = authenticated_client.get('/pedidos/desde-mensaje')
    assert response.status_code == 200
    assert b'Mensaje' in response.data

def test_choferes_list_shows_documentation_status(authenticated_client):
    response = authenticated_client.get('/recursos/choferes')
    assert response.status_code == 200
    assert b'badge' in response.data

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b'healthy' in response.data

def test_csv_export_clientes(authenticated_client):
    response = authenticated_client.get('/recursos/csv/clientes/exportar')
    assert response.status_code == 200
    assert 'text/csv' in response.content_type