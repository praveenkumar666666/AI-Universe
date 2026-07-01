from flask import Flask
from flask_socketio import SocketIO

from config import Config
from extensions import db

from routes.chat import chat, register_socket_events
from routes.auth import auth
from routes.home import home   # ✅ IMPORTANT (you were missing home)

# =========================
# APP INIT
# =========================
app = Flask(__name__)
app.config.from_object(Config)

# =========================
# EXTENSIONS INIT
# =========================
db.init_app(app)

# =========================
# SOCKET.IO INIT
# =========================
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"   # ✅ IMPORTANT for production stability
)

# =========================
# REGISTER SOCKET EVENTS
# =========================
register_socket_events(socketio)

# =========================
# BLUEPRINTS
# =========================
app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(chat)

# =========================
# MAIN RUN
# =========================
if __name__ == "__main__":
    socketio.run(
        app,
        debug=True,
        host="0.0.0.0",
        port=5000
    )