from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Universe Test</title>
    </head>
    <body style="background:black;color:white;text-align:center;padding-top:100px;">
        <h1>🚀 AI Universe is Working!</h1>
        <p>Render + Flask are working correctly.</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)