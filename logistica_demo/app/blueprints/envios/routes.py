from flask import render_template, redirect, url_for, flash
from datetime import datetime
from . import envios_bp
from app import db
from app.models import Envio, Pedido, Chofer, Vehiculo, Estado

@envios_bp.route('/')
def list_envios():
    envios = Envio.query.order_by(Envio.fecha.desc()).limit(50).all()
    return render_template('envios/list.html', envios=envios)

@envios_bp.route('/nuevo', methods=['GET', 'POST'])
def create_envio():
    from flask import request
    if request.method == 'POST':
        pedido_ids = request.form.getlist('pedidos')
        chofer_id = request.form.get('chofer')
        vehiculo_id = request.form.get('vehiculo')
        if not pedido_ids:
            flash('Seleccione al menos un pedido.', 'warning')
            return redirect(url_for('envios.create_envio'))
        estado = Estado.query.filter_by(nombre='En Tránsito', ambito='ENVIO').first()
        codigo = f'ENV-{datetime.now().strftime('%Y%m%d%H%M%S')}'
        envio = Envio(codigo=codigo, id_chofer=chofer_id if chofer_id else None, id_vehiculo=vehiculo_id if vehiculo_id else None, id_estado=estado.id)
        db.session.add(envio)
        db.session.flush()
        for pid in pedido_ids:
            pedido = Pedido.query.get(int(pid))
            if pedido:
                pedido.id_envio = envio.id
        db.session.commit()
        flash(f'Envío {codigo} creado con {len(pedido_ids)} pedido(s).', 'success')
        return redirect(url_for('envios.view_envio', id=envio.id))
    pendiente = Estado.query.filter_by(nombre='Pendiente', ambito='PEDIDO').first()
    pedidos_disponibles = Pedido.query.filter_by(id_estado=pendiente.id, id_envio=None).all() if pendiente else []
    choferes = Chofer.query.all()
    vehiculos = Vehiculo.query.all()
    return render_template('envios/form.html', pedidos=pedidos_disponibles, choferes=choferes, vehiculos=vehiculos)

@envios_bp.route('/<int:id>')
def view_envio(id):
    envio = Envio.query.get_or_404(id)
    estados = Estado.query.filter_by(ambito='ENVIO').all()
    return render_template('envios/view.html', envio=envio, estados=estados)

@envios_bp.route('/<int:id>/estado/<int:estado_id>', methods=['POST'])
def update_estado(id, estado_id):
    envio = Envio.query.get_or_404(id)
    envio.id_estado = estado_id
    db.session.commit()
    flash('Estado actualizado.', 'success')
    return redirect(url_for('envios.view_envio', id=id))