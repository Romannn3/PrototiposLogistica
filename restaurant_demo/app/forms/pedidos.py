"""Order Forms."""
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional


class PedidoForm(FlaskForm):
    id_mesa = SelectField('Mesa', validators=[DataRequired()], coerce=int)
    id_mozo = SelectField('Mozo', validators=[Optional()], coerce=int)
    notas = TextAreaField('Notas')
    submit = SubmitField('Crear Pedido')


class ItemPedidoForm(FlaskForm):
    id_plato = SelectField('Plato', validators=[DataRequired()], coerce=int)
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)], default=1)
    notas = TextAreaField('Notas (ej: sin sal, término medio)')
    submit = SubmitField('Agregar')
