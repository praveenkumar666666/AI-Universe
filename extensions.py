from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_socketio import SocketIO

# Database
db = SQLAlchemy()

# Login Manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please login to continue."

# Password Hashing
bcrypt = Bcrypt()

# Database Migration
migrate = Migrate()

# SocketIO
socketio = SocketIO()