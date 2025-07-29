from flask import Blueprint

# Blueprint instances
auth_bp = Blueprint('auth_bp', __name__)
dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/dashboard')

# Import route definitions (this attaches routes to the blueprints)
from . import auth
from . import dash


