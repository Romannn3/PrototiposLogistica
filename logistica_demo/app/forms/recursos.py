from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    celular = StringField('Celular')
    direccion = StringField('Dirección')
    localidad = StringField('Localidad')
    submit = SubmitField('Guardar')

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = StringField('Descripción')
    submit = SubmitField('Guardar')

class ChoferForm(FlaskForm):
    dni = StringField('DNI', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    celular = StringField('Celular')
    vto_licencia = DateField('Vto. Licencia', validators=[Optional()])
    vto_carnet_sanitario = DateField('Vto. Carnet Sanitario', validators=[Optional()])
    vto_seguro_personal = DateField('Vto. Seguro Personal', validators=[Optional()])
    submit = SubmitField('Guardar')

class VehiculoForm(FlaskForm):
    patente = StringField('Patente', validators=[DataRequired()])
    modelo = StringField('Modelo')
    tipo = StringField('Tipo')
    vto_vtv = DateField('Vto. VTV', validators=[Optional()])
    vto_seguro = DateField('Vto. Seguro', validators=[Optional()])
    vto_habilitacion = DateField('Vto. Habilitación', validators=[Optional()])
    submit = SubmitField('Guardar')

class CSVUploadForm(FlaskForm):
    archivo = FileField('Archivo CSV', validators=[DataRequired(), FileAllowed(['csv'], 'Solo archivos CSV permitidos.')])
    submit = SubmitField('Importar')