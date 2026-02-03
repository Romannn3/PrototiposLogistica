from . import db
from datetime import datetime, date, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='operador')
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.rol == 'admin'

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(50))
    direccion = db.Column(db.String(200))
    localidad = db.Column(db.String(100))
    pedidos = db.relationship('Pedido', backref='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.nombre}>'

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))

    def __repr__(self):
        return f'<Producto {self.nombre}>'

class Chofer(db.Model):
    __tablename__ = 'chofer'
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(50))
    vto_licencia = db.Column(db.Date)
    vto_carnet_sanitario = db.Column(db.Date)
    vto_seguro_personal = db.Column(db.Date)
    envios = db.relationship('Envio', backref='chofer', lazy=True)

    @property
    def estado_documentacion(self):
        today = date.today()
        warning_threshold = today + timedelta(days=30)
        status = {'fields': {}, 'global_status': 'success', 'alertas': [], 'avisos': []}
        campos = {'vto_licencia': 'Licencia', 'vto_carnet_sanitario': 'Carnet San.', 'vto_seguro_personal': 'Seguro'}
        any_expired = False
        any_warning = False
        for field, label in campos.items():
            valor = getattr(self, field)
            if not valor:
                status['fields'][field] = 'secondary'
                continue
            if valor < today:
                status['fields'][field] = 'danger'
                status['alertas'].append(label)
                any_expired = True
            elif valor <= warning_threshold:
                status['fields'][field] = 'warning'
                status['avisos'].append(label)
                any_warning = True
            else:
                status['fields'][field] = 'success'
        if any_expired:
            status['global_status'] = 'danger'
        elif any_warning:
            status['global_status'] = 'warning'
        return status

    def __repr__(self):
        return f'<Chofer {self.nombre} {self.apellido}>'

class Vehiculo(db.Model):
    __tablename__ = 'vehiculo'
    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(20), unique=True, nullable=False)
    modelo = db.Column(db.String(50))
    tipo = db.Column(db.String(50))
    vto_vtv = db.Column(db.Date)
    vto_seguro = db.Column(db.Date)
    vto_habilitacion = db.Column(db.Date)
    envios = db.relationship('Envio', backref='vehiculo', lazy=True)

    @property
    def estado_documentacion(self):
        today = date.today()
        warning_threshold = today + timedelta(days=30)
        status = {'fields': {}, 'global_status': 'success', 'alertas': [], 'avisos': []}
        campos = {'vto_vtv': 'VTV', 'vto_seguro': 'Seguro', 'vto_habilitacion': 'Habilitación'}
        any_expired = False
        any_warning = False
        for field, label in campos.items():
            valor = getattr(self, field)
            if not valor:
                status['fields'][field] = 'secondary'
                continue
            if valor < today:
                status['fields'][field] = 'danger'
                status['alertas'].append(label)
                any_expired = True
            elif valor <= warning_threshold:
                status['fields'][field] = 'warning'
                status['avisos'].append(label)
                any_warning = True
            else:
                status['fields'][field] = 'success'
        if any_expired:
            status['global_status'] = 'danger'
        elif any_warning:
            status['global_status'] = 'warning'
        return status

    def __repr__(self):
        return f'<Vehiculo {self.patente}>'

class Estado(db.Model):
    __tablename__ = 'estado'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    ambito = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(20), default='secondary')
    is_final = db.Column(db.Boolean, default=False)

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_entrega = db.Column(db.Date)
    lugar_entrega = db.Column(db.String(200))
    comentarios = db.Column(db.Text)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)
    id_envio = db.Column(db.Integer, db.ForeignKey('envio.id'))
    estado = db.relationship('Estado')
    items = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Pedido #{self.id} - {self.cliente.nombre}>'

class ItemPedido(db.Model):
    __tablename__ = 'item_pedido'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False, default=1)
    unidad = db.Column(db.String(20), default='unidades')
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    producto = db.relationship('Producto')

    def __repr__(self):
        return f'<ItemPedido {self.cantidad} {self.unidad} de {self.producto.nombre}>'

class Envio(db.Model):
    __tablename__ = 'envio'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    notas = db.Column(db.Text)
    id_chofer = db.Column(db.Integer, db.ForeignKey('chofer.id'))
    id_vehiculo = db.Column(db.Integer, db.ForeignKey('vehiculo.id'))
    id_estado = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)
    estado = db.relationship('Estado')
    pedidos = db.relationship('Pedido', backref='envio', lazy=True)

    def __repr__(self):
        return f'<Envio {self.codigo}>'