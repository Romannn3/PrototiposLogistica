"""Menu Blueprint."""
from flask import Blueprint

menu_bp = Blueprint('menu', __name__, template_folder='../../templates/menu')

from . import routes
