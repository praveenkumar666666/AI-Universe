from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from extensions import db, bcrypt
from models import User

from datetime import datetime
from dateutil.relativedelta import relativedelta

auth = Blueprint("auth", __name__)


# =========================
# REGISTER
# =========================
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # check existing user
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))

        # hash password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # create user
        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        # =========================
        # 🎁 6 MONTH FREE SUBSCRIPTION
        # =========================
        new_user.subscription_end = datetime.utcnow() + relativedelta(months=6)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# =========================
# LOGIN
# =========================
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        # check user exists
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User not found.", "danger")
            return redirect(url_for("auth.login"))

        # check password
        if not bcrypt.check_password_hash(user.password, password):
            flash("Incorrect password.", "danger")
            return redirect(url_for("auth.login"))

        # login success
        login_user(user)

        flash("Login successful!", "success")

        return redirect(url_for("chat.new_chat"))

    return render_template("login.html")


# =========================
# LOGOUT
# =========================
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.", "success")

    return redirect(url_for("home.index"))