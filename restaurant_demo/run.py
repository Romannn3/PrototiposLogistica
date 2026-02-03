from app import create_app, db

app = create_app()


@app.shell_context_processor
def make_shell_context():
    from app.models import Usuario, Categoria, Plato, Mesa, Pedido, ItemPedido, Estado, Personal
    return {
        'db': db,
        'Usuario': Usuario,
        'Categoria': Categoria,
        'Plato': Plato,
        'Mesa': Mesa,
        'Pedido': Pedido,
        'ItemPedido': ItemPedido,
        'Estado': Estado,
        'Personal': Personal
    }


if __name__ == '__main__':
    app.run(debug=True)
