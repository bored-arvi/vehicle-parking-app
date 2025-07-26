#app.py
from flask import Flask, render_template
from extensions import socketio
from controllers import auth_bp, dashboard_bp
from api.parking_spots_api import parking_spot_bp
from api.reservations_api import reservations_bp
from models.db_init import init_db
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Register all blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(parking_spot_bp)
app.register_blueprint(reservations_bp)
socketio.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    socketio.run(app, debug=True)
