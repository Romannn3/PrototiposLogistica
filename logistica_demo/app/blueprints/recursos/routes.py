import os
import uuid
from flask import render_template, redirect, url_for, flash, request, Response, current_app
from werkzeug.utils import secure_filename
from . import recursos_bp
from app import db
from app.models import Cliente, Producto, Chofer, Vehiculo
from app.forms.recursos import ClienteForm, ProductoForm, ChoferForm, VehiculoForm, CSVUploadForm
from app.csv_handlers import CSVProcessor, CSVHandlerFactory
from app.utils import roles_accepted

@recursos_bp.route('/clientes')
def list_clientes():
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    return render_template('recursos/clientes.html', clientes=clientes)

@recursos_bp.route('/clientes/nuevo', methods=['GET', 'POST'])
def create_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        cliente = Cliente(nombre=form.nombre.data, celular=form.celular.data, direccion=form.direccion.data, localidad=form.localidad.data)
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente creado.', 'success')
        return redirect(url_for('recursos.list_clientes'))
    return render_template('recursos/form.html', form=form, title='Nuevo Cliente')

@recursos_bp.route('/choferes')
def list_choferes():
    choferes = Chofer.query.all()
    return render_template('recursos/choferes.html', choferes=choferes)

@recursos_bp.route('/choferes/nuevo', methods=['GET', 'POST'])
@roles_accepted('admin', 'operador')
def create_chofer():
    form = ChoferForm()
    if form.validate_on_submit():
        chofer = Chofer(dni=form.dni.data, nombre=form.nombre.data, apellido=form.apellido.data, celular=form.celular.data, vto_licencia=form.vto_licencia.data, vto_carnet_sanitario=form.vto_carnet_sanitario.data, vto_seguro_personal=form.vto_seguro_personal.data)
        db.session.add(chofer)
        db.session.commit()
        flash('Chofer creado.', 'success')
        return redirect(url_for('recursos.list_choferes'))
    return render_template('recursos/chofer_form.html', form=form, title='Nuevo Chofer')

@recursos_bp.route('/choferes/<int:id>/editar', methods=['GET', 'POST'])
@roles_accepted('admin', 'operador')
def edit_chofer(id):
    chofer = Chofer.query.get_or_404(id)
    form = ChoferForm(obj=chofer)
    if form.validate_on_submit():
        form.populate_obj(chofer)
        db.session.commit()
        flash('Chofer actualizado.', 'success')
        return redirect(url_for('recursos.list_choferes'))
    return render_template('recursos/chofer_form.html', form=form, title='Editar Chofer')

@recursos_bp.route('/vehiculos')
def list_vehiculos():
    vehiculos = Vehiculo.query.all()
    return render_template('recursos/vehiculos.html', vehiculos=vehiculos)

@recursos_bp.route('/vehiculos/nuevo', methods=['GET', 'POST'])
@roles_accepted('admin', 'operador')
def create_vehiculo():
    form = VehiculoForm()
    if form.validate_on_submit():
        vehiculo = Vehiculo(patente=form.patente.data, modelo=form.modelo.data, tipo=form.tipo.data, vto_vtv=form.vto_vtv.data, vto_seguro=form.vto_seguro.data, vto_habilitacion=form.vto_habilitacion.data)
        db.session.add(vehiculo)
        db.session.commit()
        flash('Vehículo creado.', 'success')
        return redirect(url_for('recursos.list_vehiculos'))
    return render_template('recursos/vehiculo_form.html', form=form, title='Nuevo Vehículo')

@recursos_bp.route('/csv/<entity>/exportar')
def export_csv(entity):
    try:
        handler = CSVHandlerFactory.get_handler(entity)
    except ValueError:
        flash('Entidad no válida.', 'danger')
        return redirect(url_for('index'))
    queries = {'clientes': Cliente.query, 'productos': Producto.query, 'choferes': Chofer.query, 'vehiculos': Vehiculo.query}
    query = queries.get(entity)
    generator = CSVProcessor.generate_csv_stream(handler, query)
    return Response(generator(), mimetype='text/csv', headers={'Content-Disposition': f'attachment; filename={entity}.csv'})

@recursos_bp.route('/csv/<entity>/importar', methods=['GET', 'POST'])
@roles_accepted('admin')
def import_csv(entity):
    form = CSVUploadForm()
    preview_data = None
    try:
        handler = CSVHandlerFactory.get_handler(entity)
    except ValueError:
        flash('Entidad no válida.', 'danger')
        return redirect(url_for('index'))
    if form.validate_on_submit():
        file = form.archivo.data
        filename = f'{uuid.uuid4().hex}.csv'
        upload_folder = current_app.config.get('UPLOAD_FOLDER', '/tmp')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, secure_filename(filename))
        file.save(filepath)
        if 'preview' in request.form:
            preview_data = CSVProcessor.preview_import(handler, filepath)
            from flask import session
            session['csv_import_file'] = filepath
            session['csv_import_entity'] = entity
        elif 'confirmar' in request.form:
            from flask import session
            filepath = session.get('csv_import_file')
            if filepath and os.path.exists(filepath):
                result = CSVProcessor.commit_import(handler, filepath)
                flash(f'Importación completada: {result['success']} exitosos, {result['skipped']} omitidos.', 'success' if result['success'] > 0 else 'warning')
                os.remove(filepath)
                session.pop('csv_import_file', None)
                session.pop('csv_import_entity', None)
                return redirect(url_for(f'recursos.list_{entity}'))
    return render_template('recursos/csv_import.html', form=form, entity=entity, preview_data=preview_data, headers=handler.get_headers())