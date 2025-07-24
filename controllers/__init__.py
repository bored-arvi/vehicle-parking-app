from flask import Blueprint

# Blueprint instances
auth_bp = Blueprint('auth_bp', __name__)
admin_dashboard_bp = Blueprint('admin_dashboard_bp', __name__, url_prefix='/admin')

# Import route definitions (this attaches routes to the blueprints)
from . import auth
from . import dash


