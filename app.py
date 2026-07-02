from flask import Flask
from flask_socketio import SocketIO

from config import Config
from extensions import (
    db,
    bcrypt,
    login_manager,
    migrate
)

from routes.chat import chat, register_socket_events
from routes.auth import auth
from routes.home import home

# =========================
# APP INIT
# =========================
app = Flask(__name__)
app.config.from_object(Config)

# =========================
# EXTENSIONS INIT
# =========================
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
migrate.init_app(app, db)

# =========================
# SOCKET.IO INIT
# =========================
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

# =========================
# REGISTER SOCKET EVENTS
# =========================
register_socket_events(socketio)

# =========================
# REGISTER BLUEPRINTS
# =========================
app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(chat)

# =========================
# CREATE DATABASE TABLES
# =========================
with app.app_context():
    db.create_all()

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True
    )