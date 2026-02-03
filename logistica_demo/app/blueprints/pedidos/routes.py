from flask import render_template, redirect, url_for, flash, request, jsonify
from datetime import date, datetime
from . import pedidos_bp
from app import db
from app.models import Pedido, ItemPedido, Cliente, Producto, Estado
from app.forms.pedidos import PedidoForm, ItemPedidoForm, PedidoMensajeForm
from app.utils import parsear_mensaje

@pedidos_bp.route('/')
def list_pedidos():
    pedidos = Pedido.query.order_by(Pedido.fecha.desc()).limit(50).all()
    return render_template('pedidos/list.html', pedidos=pedidos)

@pedidos_bp.route('/nuevo', methods=['GET', 'POST'])
def create_pedido():
    form = PedidoForm()
    form.id_cliente.choices = [(c.id, c.nombre) for c in Cliente.query.order_by(Cliente.nombre).all()]
    if form.validate_on_submit():
        estado = Estado.query.filter_by(nombre='Pendiente', ambito='PEDIDO').first()
        pedido = Pedido(id_cliente=form.id_cliente.data, fecha_entrega=form.fecha_entrega.data, lugar_entrega=form.lugar_entrega.data, comentarios=form.comentarios.data, id_estado=estado.id)
        db.session.add(pedido)
        db.session.commit()
        flash('Pedido creado.', 'success')
        return redirect(url_for('pedidos.view_pedido', id=pedido.id))
    return render_template('pedidos/form.html', form=form)

@pedidos_bp.route('/desde-mensaje', methods=['GET', 'POST'])
def crear_desde_mensaje():
    form = PedidoMensajeForm()
    parsed_data = None
    if form.validate_on_submit():
        parsed_data = parsear_mensaje(form.mensaje.data)
        if 'confirmar' in request.form:
            try:
                cliente = Cliente.query.filter(Cliente.nombre.ilike(f'%{parsed_data['cliente']}%')).first()
                if not cliente:
                    cliente = Cliente(nombre=parsed_data['cliente'] or 'Cliente sin nombre')
                    db.session.add(cliente)
                    db.session.flush()
                estado = Estado.query.filter_by(nombre='Pendiente', ambito='PEDIDO').first()
                fecha_entrega = None
                if parsed_data['dia']:
                    dia_lower = parsed_data['dia'].lower()
                    if 'hoy' in dia_lower:
                        fecha_entrega = date.today()
                    elif 'mañana' in dia_lower:
                        from datetime import timedelta
                        fecha_entrega = date.today() + timedelta(days=1)
                pedido = Pedido(id_cliente=cliente.id, fecha_entrega=fecha_entrega, lugar_entrega=parsed_data['lugar_entrega'], comentarios=parsed_data['comentario'], id_estado=estado.id)
                db.session.add(pedido)
                db.session.flush()
                for prod_data in parsed_data['productos']:
                    producto = Producto.query.filter(Producto.nombre.ilike(f'%{prod_data['nombre']}%')).first()
                    if not producto:
                        producto = Producto(nombre=prod_data['nombre'])
                        db.session.add(producto)
                        db.session.flush()
                    item = ItemPedido(id_pedido=pedido.id, id_producto=producto.id, cantidad=prod_data['cantidad'], unidad=prod_data['unidad'])
                    db.session.add(item)
                db.session.commit()
                flash('Pedido creado exitosamente desde mensaje.', 'success')
                return redirect(url_for('pedidos.view_pedido', id=pedido.id))
            except Exception as e:
                db.session.rollback()
                flash(f'Error al crear pedido: {str(e)}', 'danger')
    return render_template('pedidos/desde_mensaje.html', form=form, parsed_data=parsed_data)

@pedidos_bp.route('/api/parse-message', methods=['POST'])
def api_parse_message():
    data = request.get_json()
    mensaje = data.get('mensaje', '')
    resultado = parsear_mensaje(mensaje)
    return jsonify(resultado)

@pedidos_bp.route('/<int:id>')
def view_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    item_form = ItemPedidoForm()
    item_form.id_producto.choices = [(p.id, p.nombre) for p in Producto.query.all()]
    estados = Estado.query.filter_by(ambito='PEDIDO').all()
    return render_template('pedidos/view.html', pedido=pedido, item_form=item_form, estados=estados)

@pedidos_bp.route('/<int:id>/agregar-item', methods=['POST'])
def add_item(id):
    form = ItemPedidoForm()
    form.id_producto.choices = [(p.id, p.nombre) for p in Producto.query.all()]
    if form.validate_on_submit():
        item = ItemPedido(id_pedido=id, id_producto=form.id_producto.data, cantidad=form.cantidad.data, unidad=form.unidad.data)
        db.session.add(item)
        db.session.commit()
        flash('Item agregado.', 'success')
    return redirect(url_for('pedidos.view_pedido', id=id))

@pedidos_bp.route('/<int:id>/estado/<int:estado_id>', methods=['POST'])
def update_estado(id, estado_id):
    pedido = Pedido.query.get_or_404(id)
    pedido.id_estado = estado_id
    db.session.commit()
    flash('Estado actualizado.', 'success')
    return redirect(url_for('pedidos.view_pedido', id=id))