from flask import Flask
from controllers import auth_bp
from models.db_init import init_db  

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session

# Register blueprint
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
