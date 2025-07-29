from flask import Blueprint

# Blueprint instances
auth_bp = Blueprint('auth_bp', __name__,url_prefix='/auth')
dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/dashboard')
register_bp = Blueprint('register_bp', __name__)

# Import route definitions (this attaches routes to the blueprints)
from . import auth
from . import dash
from . import register

