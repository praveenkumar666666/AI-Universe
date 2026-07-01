from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models import User, Conversation

home = Blueprint("home", __name__)


# =========================
# HOME PAGE
# =========================
@home.route("/")
def index():
    return render_template("index.html")


# =========================
# ADMIN PANEL (SECURE)
# =========================
@home.route("/admin")
@login_required
def admin_panel():

    # 🔒 SIMPLE ADMIN CHECK (you can improve later)
    if current_user.email != "admin@gmail.com":
        return "❌ Access Denied"

    users = User.query.all()
    conversations = Conversation.query.all()

    return render_template(
        "admin.html",
        users=users,
        conversations=conversations
    )