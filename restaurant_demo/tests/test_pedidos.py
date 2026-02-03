import pytest
from app.models import Pedido, ItemPedido, Estado


def test_list_pedidos(authenticated_client):
    response = authenticated_client.get('/pedidos/')
    assert response.status_code == 200
    assert b'Pedidos' in response.data


def test_create_pedido_page(authenticated_client):
    response = authenticated_client.get('/pedidos/nuevo')
    assert response.status_code == 200
    assert b'Nuevo' in response.data or b'Mesa' in response.data


def test_create_pedido_success(authenticated_client, app):
    with app.app_context():
        response = authenticated_client.post('/pedidos/nuevo', data={
            'id_mesa': 1,
            'id_mozo': 0,
            'notas': 'Test order'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        pedido = Pedido.query.filter_by(notas='Test order').first()
        assert pedido is not None


def test_view_pedido(authenticated_client, app):
    with app.app_context():
        from app.blueprints.pedidos.services import crear_pedido
        pedido = crear_pedido(id_mesa=1, notas='Test view')
        
        response = authenticated_client.get(f'/pedidos/{pedido.id}')
        assert response.status_code == 200


def test_add_item_to_pedido(authenticated_client, app):
    with app.app_context():
        from app.blueprints.pedidos.services import crear_pedido
        pedido = crear_pedido(id_mesa=1)
        
        response = authenticated_client.post(f'/pedidos/{pedido.id}/agregar-item', data={
            'id_plato': 1,
            'cantidad': 2,
            'notas': 'Sin sal'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        item = ItemPedido.query.filter_by(id_pedido=pedido.id).first()
        assert item is not None
        assert item.cantidad == 2


def test_change_pedido_estado(authenticated_client, app):
    with app.app_context():
        from app.blueprints.pedidos.services import crear_pedido
        pedido = crear_pedido(id_mesa=1)
        
        new_estado = Estado.query.filter(Estado.id != pedido.id_estado).first()
        
        response = authenticated_client.post(
            f'/pedidos/{pedido.id}/estado/{new_estado.id}',
            follow_redirects=True
        )
        
        assert response.status_code == 200


def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b'healthy' in response.data
