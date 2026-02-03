import pytest
from app import create_app, db
from app.models import Usuario, Categoria, Plato, Mesa, Estado, Personal


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })
    
    with app.app_context():
        db.drop_all()
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


@pytest.fixture
def sample_mesa(app):
    with app.app_context():
        mesa = Mesa.query.first()
        return mesa


@pytest.fixture
def sample_plato(app):
    with app.app_context():
        plato = Plato.query.first()
        return plato


def seed_test_data():
    admin = Usuario(username='admin', email='admin@test.com', rol='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    
    estados = [
        Estado(nombre='Pendiente', ambito='PEDIDO', color='warning'),
        Estado(nombre='En Preparación', ambito='PEDIDO', color='info'),
        Estado(nombre='Listo', ambito='PEDIDO', color='primary'),
        Estado(nombre='Entregado', ambito='PEDIDO', color='success', is_final=True)
    ]
    for e in estados:
        db.session.add(e)
    
    cat = Categoria(nombre='Entradas', descripcion='Entradas y aperitivos')
    db.session.add(cat)
    
    plato = Plato(nombre='Empanadas', precio=500, id_categoria=1, disponible=True)
    db.session.add(plato)
    
    mesa = Mesa(numero=1, capacidad=4, ubicacion='Interior')
    db.session.add(mesa)
    
    mozo = Personal(nombre='Juan', apellido='Pérez', rol='mozo', activo=True)
    db.session.add(mozo)
    
    db.session.commit()
