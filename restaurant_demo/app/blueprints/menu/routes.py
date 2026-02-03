from flask import render_template, redirect, url_for, flash, request
from . import menu_bp
from .services import crear_plato, actualizar_plato, eliminar_plato, listar_platos_por_categoria
from app.forms.menu import PlatoForm, CategoriaForm
from app.models import Categoria, Plato
from app.utils import roles_accepted


@menu_bp.route('/')
def list_menu():
    categorias = listar_platos_por_categoria()
    return render_template('menu/list.html', categorias=categorias)


@menu_bp.route('/plato/nuevo', methods=['GET', 'POST'])
@roles_accepted('admin', 'encargado')
def create_plato():
    form = PlatoForm()
    form.id_categoria.choices = [(c.id, c.nombre) for c in Categoria.query.all()]
    
    if form.validate_on_submit():
        try:
            crear_plato(
                nombre=form.nombre.data,
                precio=form.precio.data,
                id_categoria=form.id_categoria.data,
                descripcion=form.descripcion.data,
                disponible=form.disponible.data
            )
            flash('Plato creado exitosamente.', 'success')
            return redirect(url_for('menu.list_menu'))
        except ValueError as e:
            flash(str(e), 'danger')
    
    return render_template('menu/form.html', form=form, title='Nuevo Plato')


@menu_bp.route('/plato/<int:id>/editar', methods=['GET', 'POST'])
@roles_accepted('admin', 'encargado')
def edit_plato(id):
    plato = Plato.query.get_or_404(id)
    form = PlatoForm(obj=plato)
    form.id_categoria.choices = [(c.id, c.nombre) for c in Categoria.query.all()]
    
    if form.validate_on_submit():
        try:
            actualizar_plato(
                id,
                nombre=form.nombre.data,
                precio=form.precio.data,
                id_categoria=form.id_categoria.data,
                descripcion=form.descripcion.data,
                disponible=form.disponible.data
            )
            flash('Plato actualizado.', 'success')
            return redirect(url_for('menu.list_menu'))
        except ValueError as e:
            flash(str(e), 'danger')
    
    return render_template('menu/form.html', form=form, title='Editar Plato')


@menu_bp.route('/plato/<int:id>/eliminar', methods=['POST'])
@roles_accepted('admin')
def delete_plato(id):
    try:
        eliminar_plato(id)
        flash('Plato eliminado.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('menu.list_menu'))
