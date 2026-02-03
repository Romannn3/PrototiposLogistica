from datetime import date, timedelta
from app import db
from app.models import Usuario, Cliente, Producto, Chofer, Vehiculo, Estado

def init_demo_data():
    """Inicializa la base de datos con datos de demostración."""
    # En modo demo (in-memory), siempre creamos los datos si no existen
    # No verificamos Usuario.query.first() aquí porque en :memory: las tablas acaban de crearse
    try:
        if Usuario.query.first():
            return
    except Exception:
        pass # Si falla es pq no existen las tablas aun (aunque db.create_all deberia haberlas creado)

    print(' Inicializing demo database...')
    
    # Estados
    estados_pedido = [('Pendiente', 'PEDIDO', 'warning', False), ('En Preparación', 'PEDIDO', 'info', False), ('Listo para Envío', 'PEDIDO', 'primary', False), ('Entregado', 'PEDIDO', 'success', True), ('Cancelado', 'PEDIDO', 'danger', True)]
    estados_envio = [('En Tránsito', 'ENVIO', 'info', False), ('Completado', 'ENVIO', 'success', True), ('Cancelado', 'ENVIO', 'danger', True)]
    
    for nombre, ambito, color, is_final in estados_pedido + estados_envio:
        db.session.add(Estado(nombre=nombre, ambito=ambito, color=color, is_final=is_final))

    # Admin User
    admin = Usuario(username='admin', email='admin@demo.com', rol='admin')
    admin.set_password('admin123')
    db.session.add(admin)

    # Clientes
    clientes = [('Juan Pérez', '1155551234', 'Av. Corrientes 1234', 'Buenos Aires'), ('María García', '1155555678', 'Calle San Martín 567', 'Córdoba'), ('Carlos López', '1155559012', 'Av. del Libertador 890', 'Rosario')]
    for nombre, celular, direccion, localidad in clientes:
        db.session.add(Cliente(nombre=nombre, celular=celular, direccion=direccion, localidad=localidad))

    # Productos
    productos = ['Harina', 'Aceite', 'Azúcar', 'Sal', 'Leche en polvo', 'Cemento', 'Arena', 'Ladrillos']
    for p in productos:
        db.session.add(Producto(nombre=p))

    # Choferes
    today = date.today()
    choferes = [('12345678', 'Roberto', 'Gómez', '1155551111', today + timedelta(days=365), today + timedelta(days=200), today + timedelta(days=180)), ('23456789', 'Ana', 'Martínez', '1155552222', today + timedelta(days=15), today + timedelta(days=100), today + timedelta(days=90)), ('34567890', 'Pedro', 'Sánchez', '1155553333', today - timedelta(days=5), today + timedelta(days=50), today - timedelta(days=10))]
    for dni, nombre, apellido, celular, lic, carnet, seguro in choferes:
        db.session.add(Chofer(dni=dni, nombre=nombre, apellido=apellido, celular=celular, vto_licencia=lic, vto_carnet_sanitario=carnet, vto_seguro_personal=seguro))

    # Vehículos
    vehiculos = [('ABC123', 'Fiat Ducato', 'Furgón', today + timedelta(days=365), today + timedelta(days=300), today + timedelta(days=400)), ('XYZ789', 'Mercedes Sprinter', 'Furgón', today + timedelta(days=20), today + timedelta(days=150), today + timedelta(days=200)), ('QWE456', 'Ford Cargo', 'Camión', today - timedelta(days=10), today - timedelta(days=5), today + timedelta(days=100))]
    for patente, modelo, tipo, vtv, seg, hab in vehiculos:
        db.session.add(Vehiculo(patente=patente, modelo=modelo, tipo=tipo, vto_vtv=vtv, vto_seguro=seg, vto_habilitacion=hab))

    db.session.commit()
    print(' Demo database ready!')
