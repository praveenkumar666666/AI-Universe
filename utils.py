from datetime import datetime

def check_subscription(user):

    # ❌ No subscription = BLOCK (safe SaaS rule)
    if not user.subscription_end:
        return False

    # ❌ Expired subscription
    if user.subscription_end < datetime.utcnow():
        return False

    # ✅ Valid subscription
    return True