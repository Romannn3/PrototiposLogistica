import pytest
import os
import tempfile
from app.csv_handlers import CSVHandlerFactory, ClienteCSVHandler, CSVProcessor

class TestCSVHandlers:

    def test_get_handler_clientes(self):
        handler = CSVHandlerFactory.get_handler('clientes')
        assert isinstance(handler, ClienteCSVHandler)

    def test_get_handler_invalid(self):
        with pytest.raises(ValueError):
            CSVHandlerFactory.get_handler('invalid')

    def test_cliente_handler_headers(self):
        handler = ClienteCSVHandler()
        headers = handler.get_headers()
        assert 'Nombre' in headers
        assert 'Celular' in headers

    def test_cliente_handler_import_row(self, app):
        with app.app_context():
            handler = ClienteCSVHandler()
            row = {'Nombre': 'Test Import', 'Celular': '123', 'Direccion': '', 'Localidad': ''}
            cliente = handler.import_row(row)
            assert cliente.nombre == 'Test Import'

    def test_cliente_handler_import_empty_name_raises(self, app):
        with app.app_context():
            handler = ClienteCSVHandler()
            row = {'Nombre': '', 'Celular': '123'}
            with pytest.raises(ValueError):
                handler.import_row(row)

    def test_csv_preview_with_valid_file(self, app):
        with app.app_context():
            handler = ClienteCSVHandler()
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
                f.write('Nombre,Celular,Direccion,Localidad\n')
                f.write('Test1,111,Dir1,Loc1\n')
                f.write('Test2,222,Dir2,Loc2\n')
                temp_path = f.name
            try:
                result = CSVProcessor.preview_import(handler, temp_path)
                assert len(result['valid_rows']) == 2
                assert len(result['errors']) == 0
            finally:
                os.unlink(temp_path)