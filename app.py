from flask import Flask, render_template
from controllers import auth_bp, dashboard_bp
from api.parking_spots_api import parking_spot_bp
from models.db_init import init_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Register all blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(parking_spot_bp)
@app.route('/')
def home():
    return render_template('index.html')
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
