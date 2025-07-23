from flask import Blueprint

auth_bp = Blueprint('auth_bp', __name__)

# Now import all route modules
from . import auth, dash

