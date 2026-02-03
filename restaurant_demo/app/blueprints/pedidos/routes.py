from flask import render_template, redirect, url_for, flash, request
from . import pedidos_bp
from .services import crear_pedido, agregar_item, cambiar_estado, eliminar_item, listar_pedidos_activos
from app.forms.pedidos import PedidoForm, ItemPedidoForm
from app.models import Pedido, Mesa, Personal, Plato, Estado


@pedidos_bp.route('/')
def list_pedidos():
    pedidos = listar_pedidos_activos()
    return render_template('pedidos/list.html', pedidos=pedidos)


@pedidos_bp.route('/nuevo', methods=['GET', 'POST'])
def create_pedido():
    form = PedidoForm()
    form.id_mesa.choices = [(m.id, f'Mesa {m.numero}') for m in Mesa.query.all()]
    form.id_mozo.choices = [(0, 'Sin asignar')] + [
        (p.id, f'{p.nombre} {p.apellido}') 
        for p in Personal.query.filter_by(rol='mozo', activo=True).all()
    ]
    
    if form.validate_on_submit():
        try:
            id_mozo = form.id_mozo.data if form.id_mozo.data != 0 else None
            pedido = crear_pedido(
                id_mesa=form.id_mesa.data,
                id_mozo=id_mozo,
                notas=form.notas.data
            )
            flash('Pedido creado.', 'success')
            return redirect(url_for('pedidos.view_pedido', id=pedido.id))
        except ValueError as e:
            flash(str(e), 'danger')
    
    return render_template('pedidos/form.html', form=form)


@pedidos_bp.route('/<int:id>')
def view_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    item_form = ItemPedidoForm()
    item_form.id_plato.choices = [
        (p.id, f'{p.nombre} - ${p.precio}') 
        for p in Plato.query.filter_by(disponible=True).all()
    ]
    estados = Estado.query.filter_by(ambito='PEDIDO').all()
    
    return render_template('pedidos/view.html', 
                         pedido=pedido, 
                         item_form=item_form,
                         estados=estados)


@pedidos_bp.route('/<int:id>/agregar-item', methods=['POST'])
def add_item(id):
    form = ItemPedidoForm()
    form.id_plato.choices = [(p.id, p.nombre) for p in Plato.query.filter_by(disponible=True).all()]
    
    if form.validate_on_submit():
        try:
            agregar_item(
                pedido_id=id,
                id_plato=form.id_plato.data,
                cantidad=form.cantidad.data,
                notas=form.notas.data
            )
            flash('Item agregado.', 'success')
        except ValueError as e:
            flash(str(e), 'danger')
    
    return redirect(url_for('pedidos.view_pedido', id=id))


@pedidos_bp.route('/<int:id>/estado/<int:estado_id>', methods=['POST'])
def update_estado(id, estado_id):
    try:
        cambiar_estado(id, estado_id)
        flash('Estado actualizado.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('pedidos.view_pedido', id=id))


@pedidos_bp.route('/item/<int:item_id>/eliminar', methods=['POST'])
def delete_item(item_id):
    from app.models import ItemPedido
    item = ItemPedido.query.get_or_404(item_id)
    pedido_id = item.id_pedido
    
    try:
        eliminar_item(item_id)
        flash('Item eliminado.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    
    return redirect(url_for('pedidos.view_pedido', id=pedido_id))
