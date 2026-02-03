from abc import ABC, abstractmethod
import csv
import io
from app import db
from app.models import Cliente, Producto, Chofer, Vehiculo
from sqlalchemy.exc import SQLAlchemyError

class CSVHandler(ABC):

    @abstractmethod
    def get_headers(self) -> list:
        pass

    @abstractmethod
    def import_row(self, row: dict) -> object:
        pass

    @abstractmethod
    def export_row(self, entity: object) -> dict:
        pass

class ClienteCSVHandler(CSVHandler):

    def get_headers(self) -> list:
        return ['Nombre', 'Celular', 'Direccion', 'Localidad']

    def import_row(self, row: dict) -> Cliente:
        nombre = row.get('Nombre', '').strip()
        if not nombre:
            raise ValueError('El nombre del cliente es obligatorio.')
        if Cliente.query.filter(Cliente.nombre.ilike(nombre)).first():
            raise ValueError(f"El cliente '{nombre}' ya existe.")
        return Cliente(nombre=nombre, celular=row.get('Celular', ''), direccion=row.get('Direccion', ''), localidad=row.get('Localidad', ''))

    def export_row(self, cliente: Cliente) -> dict:
        return {'Nombre': cliente.nombre, 'Celular': cliente.celular or '', 'Direccion': cliente.direccion or '', 'Localidad': cliente.localidad or ''}

class ProductoCSVHandler(CSVHandler):

    def get_headers(self) -> list:
        return ['Nombre', 'Descripcion']

    def import_row(self, row: dict) -> Producto:
        nombre = row.get('Nombre', '').strip()
        if not nombre:
            raise ValueError('El nombre del producto es obligatorio.')
        if Producto.query.filter(Producto.nombre.ilike(nombre)).first():
            raise ValueError(f"El producto '{nombre}' ya existe.")
        return Producto(nombre=nombre, descripcion=row.get('Descripcion', ''))

    def export_row(self, producto: Producto) -> dict:
        return {'Nombre': producto.nombre, 'Descripcion': producto.descripcion or ''}

class ChoferCSVHandler(CSVHandler):

    def get_headers(self) -> list:
        return ['DNI', 'Nombre', 'Apellido', 'Celular']

    def import_row(self, row: dict) -> Chofer:
        dni = row.get('DNI', '').strip()
        nombre = row.get('Nombre', '').strip()
        apellido = row.get('Apellido', '').strip()
        if not nombre or not apellido:
            raise ValueError('Nombre y Apellido son obligatorios.')
        if dni and Chofer.query.filter_by(dni=dni).first():
            raise ValueError(f"El chofer con DNI '{dni}' ya existe.")
        return Chofer(dni=dni, nombre=nombre, apellido=apellido, celular=row.get('Celular', ''))

    def export_row(self, chofer: Chofer) -> dict:
        return {'DNI': chofer.dni or '', 'Nombre': chofer.nombre, 'Apellido': chofer.apellido, 'Celular': chofer.celular or ''}

class VehiculoCSVHandler(CSVHandler):

    def get_headers(self) -> list:
        return ['Patente', 'Modelo', 'Tipo']

    def import_row(self, row: dict) -> Vehiculo:
        patente = row.get('Patente', '').strip()
        if not patente:
            raise ValueError('La patente es obligatoria.')
        if Vehiculo.query.filter_by(patente=patente).first():
            raise ValueError(f"El vehículo con patente '{patente}' ya existe.")
        return Vehiculo(patente=patente, modelo=row.get('Modelo', ''), tipo=row.get('Tipo', ''))

    def export_row(self, vehiculo: Vehiculo) -> dict:
        return {'Patente': vehiculo.patente, 'Modelo': vehiculo.modelo or '', 'Tipo': vehiculo.tipo or ''}

class CSVProcessor:

    @staticmethod
    def generate_csv_stream(handler: CSVHandler, query):

        def generate():
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=handler.get_headers())
            writer.writeheader()
            output.seek(0)
            yield output.read()
            output.truncate(0)
            output.seek(0)
            batch_size = 100
            ids = [r[0] for r in query.with_entities(query.column_descriptions[0]['type'].id).all()]
            for i in range(0, len(ids), batch_size):
                batch_ids = ids[i:i + batch_size]
                model = query.column_descriptions[0]['type']
                batch = query.filter(model.id.in_(batch_ids)).all()
                for entity in batch:
                    result = handler.export_row(entity)
                    if isinstance(result, list):
                        for row in result:
                            writer.writerow(row)
                    else:
                        writer.writerow(result)
                output.seek(0)
                yield output.read()
                output.truncate(0)
                output.seek(0)
        return generate

    @staticmethod
    def preview_import(handler: CSVHandler, file_path: str) -> dict:
        valid_rows = []
        errors = []
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                headers = list(reader.fieldnames) if reader.fieldnames else []
                expected = set(handler.get_headers())
                if not expected.issubset(set(headers)):
                    missing = expected - set(headers)
                    return {'errors': [{'row': 0, 'error': f'Faltan columnas: {', '.join(missing)}'}], 'valid_rows': [], 'headers': headers}
                for i, row in enumerate(reader, start=1):
                    try:
                        handler.import_row(row)
                        if len(valid_rows) < 100:
                            valid_rows.append(row)
                    except ValueError as e:
                        if len(errors) < 50:
                            errors.append({'row': i, 'error': str(e)})
                return {'valid_rows': valid_rows, 'errors': errors, 'headers': headers}
        except Exception as e:
            return {'errors': [{'row': 0, 'error': str(e)}], 'valid_rows': [], 'headers': []}

    @staticmethod
    def commit_import(handler: CSVHandler, file_path: str) -> dict:
        success_count = 0
        skipped_count = 0
        errors = []
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=1):
                try:
                    obj = handler.import_row(row)
                    if obj:
                        db.session.add(obj)
                        db.session.commit()
                        success_count += 1
                except (ValueError, SQLAlchemyError) as e:
                    db.session.rollback()
                    skipped_count += 1
                    if len(errors) < 50:
                        errors.append(f'Fila {i}: {str(e)}')
        return {'success': success_count, 'skipped': skipped_count, 'errors': errors}

class CSVHandlerFactory:
    handlers = {'clientes': ClienteCSVHandler, 'productos': ProductoCSVHandler, 'choferes': ChoferCSVHandler, 'vehiculos': VehiculoCSVHandler}

    @classmethod
    def get_handler(cls, entity: str) -> CSVHandler:
        handler_class = cls.handlers.get(entity)
        if handler_class:
            return handler_class()
        raise ValueError(f'No handler for entity: {entity}')