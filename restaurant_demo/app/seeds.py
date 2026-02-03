from . import db
from .models import Usuario, Categoria, Plato, Mesa, Estado, Personal

def seed_data():
    """Seed the database with initial data. Must be run within an app context."""
    print("Creating tables...")
    db.create_all()
    
    # Check if already seeded
    if Usuario.query.first():
        print("Database already seeded. Skipping...")
        return
    
    print("Seeding data...")
    
    # === USERS ===
    admin = Usuario(username='admin', email='admin@restaurant.com', rol='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    
    mozo_user = Usuario(username='mozo1', email='mozo@restaurant.com', rol='mozo')
    mozo_user.set_password('mozo123')
    db.session.add(mozo_user)
    
    # === STATES ===
    estados = [
        Estado(nombre='Pendiente', ambito='PEDIDO', color='warning'),
        Estado(nombre='En Preparación', ambito='PEDIDO', color='info'),
        Estado(nombre='Listo', ambito='PEDIDO', color='primary'),
        Estado(nombre='Entregado', ambito='PEDIDO', color='success', is_final=True),
        Estado(nombre='Cancelado', ambito='PEDIDO', color='danger', is_final=True),
    ]
    for e in estados:
        db.session.add(e)
    
    # === CATEGORIES ===
    categorias = [
        Categoria(nombre='Entradas', descripcion='Entradas y aperitivos', orden=1),
        Categoria(nombre='Platos Principales', descripcion='Carnes, pastas y más', orden=2),
        Categoria(nombre='Postres', descripcion='Dulces y helados', orden=3),
        Categoria(nombre='Bebidas', descripcion='Gaseosas, jugos y más', orden=4),
    ]
    for c in categorias:
        db.session.add(c)
    
    db.session.flush()  # Get IDs
    
    # === DISHES ===
    platos = [
        # Entradas
        Plato(nombre='Empanadas (3 unidades)', precio=800, id_categoria=1),
        Plato(nombre='Tabla de Fiambres', precio=1500, id_categoria=1),
        Plato(nombre='Bruschetta', precio=650, id_categoria=1),
        # Principales
        Plato(nombre='Milanesa Napolitana', precio=2200, id_categoria=2),
        Plato(nombre='Bife de Chorizo', precio=3500, id_categoria=2),
        Plato(nombre='Ravioles Caseros', precio=1800, id_categoria=2),
        Plato(nombre='Pollo al Verdeo', precio=1900, id_categoria=2),
        # Postres
        Plato(nombre='Flan con Dulce de Leche', precio=700, id_categoria=3),
        Plato(nombre='Tiramisú', precio=850, id_categoria=3),
        Plato(nombre='Helado (3 bochas)', precio=600, id_categoria=3),
        # Bebidas
        Plato(nombre='Coca Cola', precio=400, id_categoria=4),
        Plato(nombre='Agua Mineral', precio=300, id_categoria=4),
        Plato(nombre='Cerveza Artesanal', precio=650, id_categoria=4),
    ]
    for p in platos:
        db.session.add(p)
    
    # === TABLES ===
    for i in range(1, 11):
        ubicacion = 'Terraza' if i > 7 else 'Interior'
        capacidad = 6 if i % 3 == 0 else 4
        mesa = Mesa(numero=i, capacidad=capacidad, ubicacion=ubicacion)
        db.session.add(mesa)
    
    # === STAFF ===
    personal = [
        Personal(nombre='Juan', apellido='García', rol='mozo', celular='1122334455'),
        Personal(nombre='María', apellido='López', rol='mozo', celular='1166778899'),
        Personal(nombre='Carlos', apellido='Rodríguez', rol='cocinero'),
        Personal(nombre='Ana', apellido='Martínez', rol='encargado', celular='1155443322'),
    ]
    for p in personal:
        db.session.add(p)
    
    db.session.commit()
    print("✓ Base de datos cargada exitosamente!")
    print("\nCredenciales:")
    print("  Admin: admin / admin123")
    print("  Mozo: mozo1 / mozo123")
