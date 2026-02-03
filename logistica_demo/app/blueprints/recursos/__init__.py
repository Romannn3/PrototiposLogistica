from flask import Blueprint
recursos_bp = Blueprint('recursos', __name__, template_folder='../../templates/recursos')
from . import routes