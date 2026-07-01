from datetime import datetime
from flask_login import UserMixin

from extensions import db, login_manager


# =========================
# LOGIN MANAGER
# =========================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# =========================
# USER MODEL (WITH SUBSCRIPTION)
# =========================
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # =========================
    # SUBSCRIPTION SYSTEM
    # =========================
    subscription_start = db.Column(db.DateTime, default=datetime.utcnow)

    subscription_end = db.Column(db.DateTime)

    is_active = db.Column(db.Boolean, default=True)

    plan = db.Column(db.String(50), default="trial")

    conversations = db.relationship(
        "Conversation",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"


# =========================
# CONVERSATION MODEL
# =========================
class Conversation(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), default="New Chat")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    messages = db.relationship(
        "Message",
        backref="conversation",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Conversation {self.title}>"


# =========================
# MESSAGE MODEL
# =========================
class Message(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    role = db.Column(db.String(20), nullable=False)  # user / assistant

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversation.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Message {self.role}>"