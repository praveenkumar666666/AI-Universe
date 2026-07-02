from flask import Blueprint

home = Blueprint("home", __name__)

@home.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Universe</title>
    </head>
    <body style="background:black;color:white;text-align:center;padding-top:100px;">
        <h1>🚀 AI Universe is Working!</h1>
        <h2>Flask Home Route Loaded Successfully</h2>
    </body>
    </html>
    """