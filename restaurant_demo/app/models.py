from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='mozo')
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_admin(self):
        return self.rol == 'admin'
    
    def __repr__(self):
        return f'<Usuario {self.username}>'


class Categoria(db.Model):
    __tablename__ = 'categoria'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    descripcion = db.Column(db.String(200))
    orden = db.Column(db.Integer, default=0)
    
    platos = db.relationship('Plato', backref='categoria', lazy=True)
    
    def __repr__(self):
        return f'<Categoria {self.nombre}>'


class Plato(db.Model):
    __tablename__ = 'plato'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(300))
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    disponible = db.Column(db.Boolean, default=True)
    
    items = db.relationship('ItemPedido', backref='plato', lazy=True)
    
    def __repr__(self):
        return f'<Plato {self.nombre} ${self.precio}>'


class Mesa(db.Model):
    __tablename__ = 'mesa'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    capacidad = db.Column(db.Integer, default=4)
    ubicacion = db.Column(db.String(50))
    
    pedidos = db.relationship('Pedido', backref='mesa', lazy=True)
    
    @property
    def pedido_activo(self):
        for p in self.pedidos:
            if p.estado and not p.estado.is_final:
                return p
        return None
    
    def __repr__(self):
        return f'<Mesa {self.numero}>'


class Personal(db.Model):
    __tablename__ = 'personal'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(30), nullable=False)
    celular = db.Column(db.String(50))
    activo = db.Column(db.Boolean, default=True)
    
    pedidos = db.relationship('Pedido', backref='mozo', lazy=True)
    
    def __repr__(self):
        return f'<Personal {self.nombre} {self.apellido}>'


class Estado(db.Model):
    __tablename__ = 'estado'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    ambito = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(20), default='secondary')
    is_final = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Estado {self.nombre}>'


class Pedido(db.Model):
    __tablename__ = 'pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    notas = db.Column(db.Text)
    
    id_mesa = db.Column(db.Integer, db.ForeignKey('mesa.id'), nullable=False)
    id_mozo = db.Column(db.Integer, db.ForeignKey('personal.id'))
    id_estado = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)
    
    estado = db.relationship('Estado')
    items = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade='all, delete-orphan')
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.items)
    
    def __repr__(self):
        return f'<Pedido #{self.id} Mesa {self.mesa.numero}>'


class ItemPedido(db.Model):
    __tablename__ = 'item_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    notas = db.Column(db.String(200))
    
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    id_plato = db.Column(db.Integer, db.ForeignKey('plato.id'), nullable=False)
    
    @property
    def subtotal(self):
        return self.cantidad * self.plato.precio
    
    def __repr__(self):
        return f'<ItemPedido {self.cantidad}x {self.plato.nombre}>'
