from flask import Blueprint
pedidos_bp = Blueprint('pedidos', __name__, template_folder='../../templates/pedidos')
from . import routes