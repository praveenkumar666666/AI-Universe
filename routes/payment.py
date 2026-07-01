from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from datetime import datetime
from dateutil.relativedelta import relativedelta

from config import Config
from extensions import db

payment = Blueprint("payment", __name__)


# =========================
# CREATE ORDER
# =========================
@payment.route("/create-order")
@login_required
def create_order():

    amount = 49900  # ₹499 in paise

    order = Config.client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return render_template(
        "payment.html",
        order=order,
        key=Config.RAZORPAY_KEY_ID
    )


# =========================
# PAYMENT SUCCESS
# =========================
@payment.route("/payment-success", methods=["POST"])
@login_required
def payment_success():

    # 🔥 EXTEND SUBSCRIPTION
    current_user.subscription_end = datetime.utcnow() + relativedelta(months=6)

    db.session.commit()

    return "Payment Successful! Subscription extended."