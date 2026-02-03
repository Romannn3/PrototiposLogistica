import pytest
from app.models import Plato, Categoria


def test_list_menu(authenticated_client):
    response = authenticated_client.get('/menu/')
    assert response.status_code == 200
    assert 'Menú'.encode('utf-8') in response.data or b'menu' in response.data.lower()


def test_create_plato_page(authenticated_client):
    response = authenticated_client.get('/menu/plato/nuevo')
    assert response.status_code == 200
    assert b'Nuevo' in response.data or b'form' in response.data.lower()


def test_create_plato_success(authenticated_client, app):
    with app.app_context():
        response = authenticated_client.post('/menu/plato/nuevo', data={
            'nombre': 'Milanesa',
            'descripcion': 'Milanesa de carne',
            'precio': 1500.00,
            'id_categoria': 1,
            'disponible': True
        }, follow_redirects=True)
        
        assert response.status_code == 200
        plato = Plato.query.filter_by(nombre='Milanesa').first()
        assert plato is not None
        assert plato.precio == 1500.00


def test_edit_plato(authenticated_client, app, sample_plato):
    with app.app_context():
        plato = Plato.query.first()
        response = authenticated_client.get(f'/menu/plato/{plato.id}/editar')
        assert response.status_code == 200


def test_menu_displays_categories(authenticated_client, app):
    with app.app_context():
        response = authenticated_client.get('/menu/')
        assert b'Entradas' in response.data
