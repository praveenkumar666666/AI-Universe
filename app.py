from flask import Flask
from flask_socketio import SocketIO

from config import Config
from extensions import (
    db,
    bcrypt,
    login_manager,
    migrate
)

from routes.home import home
from routes.auth import auth
from routes.chat import chat, register_socket_events

socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Initialize SocketIO
    socketio.init_app(app, async_mode="eventlet")

    # Register socket events
    register_socket_events(socketio)

    # Register blueprints
    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(chat)

    # Create database
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True
    )