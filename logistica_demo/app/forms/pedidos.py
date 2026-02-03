from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, DateField, DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

class PedidoForm(FlaskForm):
    id_cliente = SelectField('Cliente', validators=[DataRequired()], coerce=int)
    fecha_entrega = DateField('Fecha Entrega', validators=[Optional()])
    lugar_entrega = StringField('Lugar de Entrega')
    comentarios = TextAreaField('Comentarios')
    submit = SubmitField('Crear Pedido')

class ItemPedidoForm(FlaskForm):
    id_producto = SelectField('Producto', validators=[DataRequired()], coerce=int)
    cantidad = DecimalField('Cantidad', validators=[DataRequired(), NumberRange(min=0.01)], default=1)
    unidad = StringField('Unidad', default='unidades')
    submit = SubmitField('Agregar')

class PedidoMensajeForm(FlaskForm):
    mensaje = TextAreaField('Mensaje', validators=[DataRequired()], render_kw={'rows': 10, 'placeholder': '📅 Día: hoy\n👤 Cliente: Juan Pérez\n📦 Productos: \n100 kg de Harina\n50 litros de Aceite\n📍 Lugar de entrega: Av. Siempreviva 742\nComentario: entregar por la mañana'})
    submit = SubmitField('Procesar Mensaje')