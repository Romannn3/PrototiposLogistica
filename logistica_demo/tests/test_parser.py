import pytest
from app.utils import parsear_mensaje

class TestParsearMensaje:

    def test_parse_complete_message(self):
        mensaje = '📅 Día: hoy\n👤 Cliente: Juan Pérez\n📦 Productos: \n100 kg de Harina\n50 litros de Aceite\n📍 Lugar de entrega: Av. Siempreviva 742\nComentario: entregar por la mañana'
        result = parsear_mensaje(mensaje)
        assert result['dia'] == 'hoy'
        assert result['cliente'] == 'Juan Pérez'
        assert result['lugar_entrega'] == 'Av. Siempreviva 742'
        assert result['comentario'] == 'entregar por la mañana'
        assert len(result['productos']) == 2
        assert result['productos'][0]['cantidad'] == 100
        assert result['productos'][0]['unidad'] == 'kg'
        assert result['productos'][0]['nombre'] == 'Harina'

    def test_parse_message_without_emojis(self):
        mensaje = 'Día: mañana\nCliente: María López\nProductos:\n20 bolsas de Cemento\nLugar de entrega: Calle Falsa 123'
        result = parsear_mensaje(mensaje)
        assert result['dia'] == 'mañana'
        assert result['cliente'] == 'María López'
        assert len(result['productos']) >= 1

    def test_parse_decimal_quantities(self):
        mensaje = '📦 Productos:\n2.5 kg de Queso\n0,75 litros de Leche'
        result = parsear_mensaje(mensaje)
        assert len(result['productos']) == 2
        assert result['productos'][0]['cantidad'] == 2.5
        assert result['productos'][1]['cantidad'] == 0.75

    def test_parse_empty_message(self):
        result = parsear_mensaje('')
        assert result['dia'] is None
        assert result['cliente'] is None
        assert result['productos'] == []

    def test_products_without_unit(self):
        mensaje = '📦 Productos:\n10 Cajas de Vino\n5 Paquetes'
        result = parsear_mensaje(mensaje)
        assert len(result['productos']) >= 1

class TestDocumentacionStatus:

    def test_chofer_documentacion_expired(self, app):
        from app.models import Chofer
        from datetime import date, timedelta
        with app.app_context():
            chofer = Chofer.query.first()
            estado = chofer.estado_documentacion
            assert estado['global_status'] == 'warning'
            assert 'Licencia' in estado['avisos']

    def test_vehiculo_documentacion_expired(self, app):
        from app.models import Vehiculo
        with app.app_context():
            vehiculo = Vehiculo.query.first()
            estado = vehiculo.estado_documentacion
            assert estado['global_status'] == 'danger'
            assert 'VTV' in estado['alertas']