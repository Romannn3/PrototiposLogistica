"""Menu Forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional


class CategoriaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    submit = SubmitField('Guardar')


class PlatoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    precio = DecimalField('Precio', validators=[DataRequired(), NumberRange(min=0.01)])
    id_categoria = SelectField('Categoría', validators=[DataRequired()], coerce=int)
    disponible = BooleanField('Disponible', default=True)
    submit = SubmitField('Guardar')
