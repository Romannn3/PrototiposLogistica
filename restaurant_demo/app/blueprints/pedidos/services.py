from app import db
from app.models import Pedido, ItemPedido, Estado, Mesa
from sqlalchemy.exc import SQLAlchemyError


def crear_pedido(id_mesa, id_mozo=None, notas=''):
    estado = Estado.query.filter_by(nombre='Pendiente', ambito='PEDIDO').first()
    if not estado:
        raise ValueError("Estado 'Pendiente' no configurado en el sistema.")
    
    try:
        pedido = Pedido(
            id_mesa=id_mesa,
            id_mozo=id_mozo,
            id_estado=estado.id,
            notas=notas
        )
        db.session.add(pedido)
        db.session.commit()
        return pedido
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Error al crear pedido: {str(e)}")


def agregar_item(pedido_id, id_plato, cantidad=1, notas=''):
    pedido = Pedido.query.get_or_404(pedido_id)
    
    try:
        item = ItemPedido(
            id_pedido=pedido_id,
            id_plato=id_plato,
            cantidad=cantidad,
            notas=notas
        )
        db.session.add(item)
        db.session.commit()
        return item
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Error al agregar item: {str(e)}")


def cambiar_estado(pedido_id, nuevo_estado_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    try:
        pedido.id_estado = nuevo_estado_id
        db.session.commit()
        return pedido
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Error al cambiar estado: {str(e)}")


def eliminar_item(item_id):
    item = ItemPedido.query.get_or_404(item_id)
    try:
        db.session.delete(item)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Error al eliminar item: {str(e)}")


def listar_pedidos_activos():
    return Pedido.query.join(Estado).filter(Estado.is_final == False).order_by(Pedido.fecha.desc()).all()
