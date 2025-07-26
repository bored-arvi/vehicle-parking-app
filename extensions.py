#extensions.py
from flask_socketio import SocketIO

socketio=SocketIO(cors_allowed_origins="*")  # if using Flask app