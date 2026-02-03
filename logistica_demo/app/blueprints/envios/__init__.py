from flask import Blueprint
envios_bp = Blueprint('envios', __name__, template_folder='../../templates/envios')
from . import routes