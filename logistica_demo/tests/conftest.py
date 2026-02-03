import pytest
from datetime import date, timedelta
from app import create_app, db
from app.models import Usuario, Cliente, Producto, Chofer, Vehiculo, Estado

@pytest.fixture
def app():
    test_config = {'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:', 'WTF_CSRF_ENABLED': False}
    app = create_app(test_config)
    with app.app_context():
        db.create_all()
        seed_test_data()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def authenticated_client(app, client):
    with client.session_transaction() as sess:
        user = Usuario.query.filter_by(username='admin').first()
        sess['_user_id'] = str(user.id)
    return client

def seed_test_data():
    admin = Usuario(username='admin', email='admin@test.com', rol='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    estados = [Estado(nombre='Pendiente', ambito='PEDIDO', color='warning'), Estado(nombre='Entregado', ambito='PEDIDO', color='success', is_final=True), Estado(nombre='En Tránsito', ambito='ENVIO', color='info'), Estado(nombre='Completado', ambito='ENVIO', color='success', is_final=True)]
    for e in estados:
        db.session.add(e)
    cliente = Cliente(nombre='Cliente Test', celular='123456')
    db.session.add(cliente)
    producto = Producto(nombre='Producto Test')
    db.session.add(producto)
    chofer = Chofer(dni='12345678', nombre='Juan', apellido='Test', vto_licencia=date.today() + timedelta(days=10))
    db.session.add(chofer)
    vehiculo = Vehiculo(patente='ABC123', vto_vtv=date.today() - timedelta(days=5))
    db.session.add(vehiculo)
    db.session.commit()