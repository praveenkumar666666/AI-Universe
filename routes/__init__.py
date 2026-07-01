from flask import Flask

from .auth import auth
from .chat import chat
from .home import home
from .payment import payment
def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth)
    app.register_blueprint(chat)
    app.register_blueprint(home)
    app.register_blueprint(payment)
    return app
