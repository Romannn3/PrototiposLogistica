from app import db
from app.models import Categoria, Plato
from sqlalchemy.exc import SQLAlchemyError


def crear_categoria(nombre, descripcion=''):
    try:
        categoria = Categoria(nombre=nombre, descripcion=descripcion)
        db.session.add(categoria)
        db.session.commit()
        return categoria
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Error al crear categoría: {str(e)}")


def crear_plato(nombre, precio, id_categoria, descripcion='', disponible=True):
    try:
        plato = Plato(
            nombre=nombre,
            precio=precio,
            id_categoria=id_categoria,
            descripcion=descripcion,
            disponible=disponible
        )
        db.session.add(plato)
        db.session.commit()
        return plato
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Error al crear plato: {str(e)}")


def actualizar_plato(plato_id, **kwargs):
    plato = Plato.query.get_or_404(plato_id)
    try:
        for key, value in kwargs.items():
            if hasattr(plato, key):
                setattr(plato, key, value)
        db.session.commit()
        return plato
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Error al actualizar plato: {str(e)}")


def eliminar_plato(plato_id):
    plato = Plato.query.get_or_404(plato_id)
    try:
        db.session.delete(plato)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Error al eliminar plato: {str(e)}")


def listar_platos_por_categoria():
    categorias = Categoria.query.order_by(Categoria.orden).all()
    return categorias
