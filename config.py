import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # =========================
    # FLASK CORE
    # =========================
    SECRET_KEY = os.getenv("SECRET_KEY", "ai_universe_secret")

    # =========================
    # DATABASE
    # =========================
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================
    # OLLAMA AI MODEL
    # =========================
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

    # =========================
    # RAZORPAY PAYMENT SYSTEM
    # =========================
    RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")

    # =========================
    # SUBSCRIPTION SETTINGS
    # =========================
    FREE_TRIAL_MONTHS = 6
    PAID_PLAN_MONTHS = 6
    PLAN_PRICE_INR = 499

    # =========================
    # SAFE RAZORPAY CLIENT
    # =========================
    @staticmethod
    def get_razorpay_client():
        import razorpay

        if not Config.RAZORPAY_KEY_ID or not Config.RAZORPAY_KEY_SECRET:
            raise Exception("❌ Razorpay keys are missing in environment variables!")

        return razorpay.Client(
            auth=(Config.RAZORPAY_KEY_ID, Config.RAZORPAY_KEY_SECRET)
        )