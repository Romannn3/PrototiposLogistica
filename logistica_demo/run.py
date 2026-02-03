from app import create_app, db
app = create_app()

@app.shell_context_processor
def make_shell_context():
    from app.models import Usuario, Cliente, Producto, Pedido, ItemPedido, Chofer, Vehiculo, Envio, Estado
    return {'db': db, 'Usuario': Usuario, 'Cliente': Cliente, 'Producto': Producto, 'Pedido': Pedido, 'ItemPedido': ItemPedido, 'Chofer': Chofer, 'Vehiculo': Vehiculo, 'Envio': Envio, 'Estado': Estado}
if __name__ == '__main__':
    app.run(debug=True)