from datetime import date, timedelta
from app import create_app, db
from app.models import Usuario, Cliente, Producto, Chofer, Vehiculo, Estado

def seed_database():
    print(' Initializing database...')
    estados_pedido = [('Pendiente', 'PEDIDO', 'warning', False), ('En Preparación', 'PEDIDO', 'info', False), ('Listo para Envío', 'PEDIDO', 'primary', False), ('Entregado', 'PEDIDO', 'success', True), ('Cancelado', 'PEDIDO', 'danger', True)]
    estados_envio = [('En Tránsito', 'ENVIO', 'info', False), ('Completado', 'ENVIO', 'success', True), ('Cancelado', 'ENVIO', 'danger', True)]
    for nombre, ambito, color, is_final in estados_pedido + estados_envio:
        if not Estado.query.filter_by(nombre=nombre, ambito=ambito).first():
            db.session.add(Estado(nombre=nombre, ambito=ambito, color=color, is_final=is_final))
    print(' Estados creados')
    if not Usuario.query.filter_by(username='admin').first():
        admin = Usuario(username='admin', email='admin@demo.com', rol='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        print(' Admin user creado (admin/admin123)')
    clientes = [('Juan Pérez', '1155551234', 'Av. Corrientes 1234', 'Buenos Aires'), ('María García', '1155555678', 'Calle San Martín 567', 'Córdoba'), ('Carlos López', '1155559012', 'Av. del Libertador 890', 'Rosario')]
    for nombre, celular, direccion, localidad in clientes:
        if not Cliente.query.filter_by(nombre=nombre).first():
            db.session.add(Cliente(nombre=nombre, celular=celular, direccion=direccion, localidad=localidad))
    print(' Clientes creados')
    productos = ['Harina', 'Aceite', 'Azúcar', 'Sal', 'Leche en polvo', 'Cemento', 'Arena', 'Ladrillos']
    for p in productos:
        if not Producto.query.filter_by(nombre=p).first():
            db.session.add(Producto(nombre=p))
    print(' Productos creados')
    today = date.today()
    choferes = [('12345678', 'Roberto', 'Gómez', '1155551111', today + timedelta(days=365), today + timedelta(days=200), today + timedelta(days=180)), ('23456789', 'Ana', 'Martínez', '1155552222', today + timedelta(days=15), today + timedelta(days=100), today + timedelta(days=90)), ('34567890', 'Pedro', 'Sánchez', '1155553333', today - timedelta(days=5), today + timedelta(days=50), today - timedelta(days=10))]
    for dni, nombre, apellido, celular, lic, carnet, seguro in choferes:
        if not Chofer.query.filter_by(dni=dni).first():
            db.session.add(Chofer(dni=dni, nombre=nombre, apellido=apellido, celular=celular, vto_licencia=lic, vto_carnet_sanitario=carnet, vto_seguro_personal=seguro))
    print(' Choferes creados (con variedad de documentos)')
    vehiculos = [('ABC123', 'Fiat Ducato', 'Furgón', today + timedelta(days=365), today + timedelta(days=300), today + timedelta(days=400)), ('XYZ789', 'Mercedes Sprinter', 'Furgón', today + timedelta(days=20), today + timedelta(days=150), today + timedelta(days=200)), ('QWE456', 'Ford Cargo', 'Camión', today - timedelta(days=10), today - timedelta(days=5), today + timedelta(days=100))]
    for patente, modelo, tipo, vtv, seg, hab in vehiculos:
        if not Vehiculo.query.filter_by(patente=patente).first():
            db.session.add(Vehiculo(patente=patente, modelo=modelo, tipo=tipo, vto_vtv=vtv, vto_seguro=seg, vto_habilitacion=hab))
    print(' Vehículos creados (con variedad de documentos)')
    db.session.commit()
    print('\n Base de datos lista!')
    print('   Login: admin / admin123')
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_database()